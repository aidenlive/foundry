"""`foundry validate` — verify the configuration tree against its schemas and
a set of cross-cutting invariants.

Structural validation uses the JSON Schemas in ``config/schema``; if the
``jsonschema`` package is unavailable, a reduced structural check runs
instead so validation never silently passes.
"""

from __future__ import annotations

import ipaddress
import json
from dataclasses import dataclass
from pathlib import Path

from . import config as cfg

SCHEMA_BY_KIND = {
    "Organization": "organization.schema.json",
    "Project": "project.schema.json",
    "Environment": "environment.schema.json",
}


@dataclass
class Finding:
    severity: str  # "error" | "warning"
    location: str
    message: str

    def __str__(self) -> str:  # pragma: no cover - formatting only
        return f"{self.severity.upper():7s} {self.location}: {self.message}"


def _schema_registry(schema_dir: Path):
    """Build a jsonschema validator factory that resolves cross-file $refs."""
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    resources = []
    for path in schema_dir.glob("*.schema.json"):
        contents = json.loads(path.read_text(encoding="utf-8"))
        resources.append((contents["$id"], Resource.from_contents(contents)))
    registry = Registry().with_resources(resources)

    def validator_for(schema_file: str) -> Draft202012Validator:
        schema = json.loads((schema_dir / schema_file).read_text(encoding="utf-8"))
        return Draft202012Validator(schema, registry=registry)

    return validator_for


def _basic_structural_check(doc: dict, kind: str, location: str, out: list[Finding]) -> None:
    if doc.get("apiVersion") != "foundry/v1":
        out.append(Finding("error", location, "apiVersion must be 'foundry/v1'"))
    if doc.get("kind") != kind:
        out.append(Finding("error", location, f"kind must be '{kind}'"))
    name = doc.get("metadata", {}).get("name", "")
    if not isinstance(name, str) or not name:
        out.append(Finding("error", location, "metadata.name is required"))


def validate_workspace(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    schema_dir = root / cfg.CONFIG_DIR / "schema"

    try:
        validator_for = _schema_registry(schema_dir) if schema_dir.is_dir() else None
    except ImportError:  # jsonschema not installed — degrade, loudly
        validator_for = None
        findings.append(
            Finding(
                "warning",
                "environment",
                "python package 'jsonschema' not installed; running reduced structural checks",
            )
        )

    documents: list[tuple[Path, str]] = [(cfg.org_path(root), "Organization")]
    documents += [(cfg.project_path(root, p), "Project") for p in cfg.list_projects(root)]
    documents += [
        (cfg.environment_path(root, e), "Environment") for e in cfg.list_environments(root)
    ]

    parsed: dict[Path, dict] = {}
    for path, kind in documents:
        location = cfg._rel(root, path)
        try:
            doc = cfg.load_yaml(path)
        except cfg.ConfigError as exc:
            findings.append(Finding("error", location, str(exc)))
            continue
        parsed[path] = doc
        if validator_for is not None:
            for err in validator_for(SCHEMA_BY_KIND[kind]).iter_errors(doc):
                where = ".".join(str(p) for p in err.absolute_path) or "(document)"
                findings.append(Finding("error", location, f"{where}: {err.message}"))
        else:
            _basic_structural_check(doc, kind, location, findings)

    findings += _check_cidrs(root, parsed)
    findings += _check_naming(root, parsed)
    findings += _check_project_stacks(root, parsed)
    findings += _check_secrets_hygiene(root)
    return findings


# --------------------------------------------------------------------------- #
# Cross-cutting invariants
# --------------------------------------------------------------------------- #
def _check_cidrs(root: Path, parsed: dict[Path, dict]) -> list[Finding]:
    findings: list[Finding] = []
    org = parsed.get(cfg.org_path(root), {})
    supernet_str = org.get("spec", {}).get("network", {}).get("cidr")
    supernet = None
    if supernet_str:
        try:
            supernet = ipaddress.ip_network(supernet_str)
        except ValueError:
            findings.append(
                Finding(
                    "error", "config/foundry.yaml",
                    f"spec.network.cidr invalid: {supernet_str}",
                )
            )

    seen: list[tuple[str, ipaddress.IPv4Network]] = []
    for env in cfg.list_environments(root):
        path = cfg.environment_path(root, env)
        location = cfg._rel(root, path)
        cidr_str = parsed.get(path, {}).get("spec", {}).get("network", {}).get("cidr")
        if not cidr_str:
            continue
        try:
            net = ipaddress.ip_network(cidr_str)
        except ValueError:
            findings.append(Finding("error", location, f"spec.network.cidr invalid: {cidr_str}"))
            continue
        if supernet and not net.subnet_of(supernet):
            findings.append(
                Finding("error", location, f"{net} is outside the org supernet {supernet}")
            )
        for other_env, other in seen:
            if net.overlaps(other):
                findings.append(
                    Finding(
                        "error", location,
                        f"{net} overlaps environment '{other_env}' ({other})",
                    )
                )
        seen.append((env, net))
    return findings


def _check_naming(root: Path, parsed: dict[Path, dict]) -> list[Finding]:
    findings: list[Finding] = []
    org = parsed.get(cfg.org_path(root), {})
    pattern = org.get("spec", {}).get("naming", {}).get("pattern", "")
    allowed = {"org", "project", "environment", "component"}
    tokens = {t.split("}")[0] for t in pattern.split("{")[1:]} if pattern else set()
    for token in tokens - allowed:
        findings.append(
            Finding(
                "error", "config/foundry.yaml",
                f"naming.pattern has unknown token '{{{token}}}'",
            )
        )
    return findings


def _check_project_stacks(root: Path, parsed: dict[Path, dict]) -> list[Finding]:
    findings: list[Finding] = []
    for project in cfg.list_projects(root):
        path = cfg.project_path(root, project)
        for stack in parsed.get(path, {}).get("spec", {}).get("stacks", []) or []:
            candidates = (root / "stacks" / project / stack, root / "stacks" / stack)
            if not any(c.is_dir() for c in candidates):
                findings.append(
                    Finding(
                        "warning",
                        cfg._rel(root, path),
                        f"declares stack '{stack}' but stacks/{project}/{stack} "
                        f"and stacks/{stack} do not exist",
                    )
                )
    return findings


def _check_secrets_hygiene(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    secrets_dir = root / cfg.CONFIG_DIR / "secrets"
    if not secrets_dir.is_dir():
        return findings
    for path in secrets_dir.rglob("*.y*ml"):
        if path.name.endswith((".enc.yaml", ".enc.yml")):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "sops" in text and "ENC[" in text:
            continue  # sops-encrypted despite the extension
        findings.append(
            Finding(
                "error",
                cfg._rel(root, path),
                "plaintext YAML in config/secrets — encrypt with "
                "`foundry secrets encrypt` (sops) or remove it",
            )
        )
    return findings
