"""Foundry configuration engine.

Implements the layered configuration model that makes ``config/`` the single
source of truth:

    org (config/foundry.yaml)
      < project (config/projects/<name>.yaml)
        < environment (config/environments/<name>.yaml)
          < local (foundry.local.yaml, git-ignored)

Maps are deep-merged, lists and scalars are replaced, and every leaf value
remembers which file it came from (its *origin*), so ``foundry config get``
can always answer "why is this value what it is?".
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = "config"
ORG_FILE = "foundry.yaml"
LOCAL_FILE = "foundry.local.yaml"
KNOWN_PROVIDERS = ("aws", "gcp", "azure", "digitalocean")


class ConfigError(RuntimeError):
    """Raised for unusable configuration or an unlocatable workspace."""


# --------------------------------------------------------------------------- #
# Workspace discovery and loading
# --------------------------------------------------------------------------- #
def find_root(start: Path | None = None) -> Path:
    """Walk upward from *start* until a directory containing
    ``config/foundry.yaml`` is found."""
    here = (start or Path.cwd()).resolve()
    for candidate in (here, *here.parents):
        if (candidate / CONFIG_DIR / ORG_FILE).is_file():
            return candidate
    raise ConfigError(
        "not inside a Foundry workspace (no config/foundry.yaml found in this "
        "directory or any parent). Run `foundry init` to create one."
    )


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{path}: invalid YAML: {exc}") from exc
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: top-level value must be a mapping")
    return data


def _document(path: Path, expected_kind: str) -> dict[str, Any]:
    doc = load_yaml(path)
    kind = doc.get("kind")
    if kind != expected_kind:
        raise ConfigError(f"{path}: expected kind '{expected_kind}', found '{kind}'")
    if not isinstance(doc.get("metadata"), dict) or "name" not in doc["metadata"]:
        raise ConfigError(f"{path}: metadata.name is required")
    doc.setdefault("spec", {})
    return doc


def org_path(root: Path) -> Path:
    return root / CONFIG_DIR / ORG_FILE


def project_path(root: Path, name: str) -> Path:
    return root / CONFIG_DIR / "projects" / f"{name}.yaml"


def environment_path(root: Path, name: str) -> Path:
    return root / CONFIG_DIR / "environments" / f"{name}.yaml"


def list_projects(root: Path) -> list[str]:
    directory = root / CONFIG_DIR / "projects"
    return sorted(p.stem for p in directory.glob("*.yaml")) if directory.is_dir() else []


def list_environments(root: Path) -> list[str]:
    directory = root / CONFIG_DIR / "environments"
    return sorted(p.stem for p in directory.glob("*.yaml")) if directory.is_dir() else []


# --------------------------------------------------------------------------- #
# Deep merge with provenance
# --------------------------------------------------------------------------- #
def _record_origin(origins: dict[str, str], path: str, value: Any, source: str) -> None:
    if isinstance(value, dict) and value:
        for key, child in value.items():
            _record_origin(origins, f"{path}.{key}" if path else key, child, source)
    else:
        origins[path] = source


def merge_layer(
    base: dict[str, Any],
    overlay: dict[str, Any],
    origins: dict[str, str],
    source: str,
    _path: str = "",
) -> None:
    """Merge *overlay* into *base* in place. Maps merge recursively; lists and
    scalars replace. Records *source* as the origin of every value it sets."""
    for key, value in overlay.items():
        path = f"{_path}.{key}" if _path else key
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            merge_layer(base[key], value, origins, source, path)
        else:
            base[key] = copy.deepcopy(value)
            _record_origin(origins, path, value, source)


def merge_layers(layers: list[tuple[str, dict[str, Any]]]) -> tuple[dict[str, Any], dict[str, str]]:
    merged: dict[str, Any] = {}
    origins: dict[str, str] = {}
    for source, layer in layers:
        merge_layer(merged, layer, origins, source)
    return merged, origins


def get_path(data: dict[str, Any], dotted: str) -> Any:
    node: Any = data
    for part in dotted.split("."):
        if not isinstance(node, dict) or part not in node:
            raise KeyError(dotted)
        node = node[part]
    return node


# --------------------------------------------------------------------------- #
# Context rendering
# --------------------------------------------------------------------------- #
def _resolve_provider(spec: dict[str, Any]) -> str:
    cloud = spec.get("cloud", {})
    provider = cloud.get("provider") or cloud.get("defaultProvider")
    if not provider:
        raise ConfigError("no cloud provider configured (spec.cloud.provider / defaultProvider)")
    if provider not in KNOWN_PROVIDERS:
        raise ConfigError(f"unknown provider '{provider}' (known: {', '.join(KNOWN_PROVIDERS)})")
    return provider


def _resolve_region(spec: dict[str, Any], provider: str) -> str:
    cloud = spec.get("cloud", {})
    if cloud.get("region"):
        return str(cloud["region"])
    defaults = cloud.get("providers", {}).get(provider, {})
    return str(defaults.get("region") or defaults.get("location") or "")


def name_for(spec: dict[str, Any], org: str, project: str, environment: str, component: str) -> str:
    naming = spec.get("naming", {})
    pattern = naming.get("pattern", "{org}-{project}-{environment}-{component}")
    delimiter = naming.get("delimiter", "-")
    name = pattern.format(org=org, project=project, environment=environment, component=component)
    while delimiter and (delimiter + delimiter) in name:
        name = name.replace(delimiter + delimiter, delimiter)
    return name.strip(delimiter)


def render_context(
    root: Path, project: str, environment: str
) -> tuple[dict[str, Any], dict[str, str]]:
    """Merge org → project → environment → local and derive computed values.

    Returns ``(context, origins)`` where *origins* maps dotted spec paths to
    the file that last set them.
    """
    org_doc = _document(org_path(root), "Organization")

    proj_file = project_path(root, project)
    if not proj_file.is_file():
        known = ", ".join(list_projects(root)) or "none defined"
        raise ConfigError(f"unknown project '{project}' (known: {known})")
    proj_doc = _document(proj_file, "Project")

    env_file = environment_path(root, environment)
    if not env_file.is_file():
        known = ", ".join(list_environments(root)) or "none defined"
        raise ConfigError(f"unknown environment '{environment}' (known: {known})")
    env_doc = _document(env_file, "Environment")

    layers: list[tuple[str, dict[str, Any]]] = [
        (_rel(root, org_path(root)), org_doc["spec"]),
        (_rel(root, proj_file), proj_doc["spec"]),
        (_rel(root, env_file), env_doc["spec"]),
    ]
    local_file = root / LOCAL_FILE
    if local_file.is_file():
        local_doc = load_yaml(local_file)
        layers.append((LOCAL_FILE, local_doc.get("spec", local_doc)))

    spec, origins = merge_layers(layers)

    org_name = str(org_doc["metadata"]["name"])
    provider = _resolve_provider(spec)
    region = _resolve_region(spec, provider)

    labels = dict(spec.get("labels", {}))
    labels.setdefault("managed-by", "foundry")
    labels["org"] = org_name
    labels["project"] = project
    labels["environment"] = environment

    context: dict[str, Any] = {
        "foundry": {"apiVersion": "foundry/v1", "renderedBy": "foundry config render"},
        "org": org_doc["metadata"],
        "project": proj_doc["metadata"],
        "environment": env_doc["metadata"],
        "spec": spec,
        "computed": {
            "provider": provider,
            "region": region,
            "tier": spec.get("tier", "nonproduction"),
            "name_prefix": name_for(spec, org_name, project, environment, ""),
            "labels": {k: str(v) for k, v in labels.items()},
            "state_key_prefix": f"{org_name}/{project}/{environment}",
        },
    }
    return context, origins


def _rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
