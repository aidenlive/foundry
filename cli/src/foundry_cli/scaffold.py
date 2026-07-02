"""`foundry new` — scaffold projects from the templates in ``templates/``.

Templates are ordinary directory trees plus a ``template.yaml`` manifest.
Rendering is deliberately boring:

* file contents: ``{{ foundry.<var> }}`` tokens are substituted; the
  ``foundry.`` prefix keeps them from colliding with GitHub Actions
  ``${{ ... }}`` expressions and Helm/Go templates,
* file paths: ``__<var>__`` segments are substituted,
* unknown tokens are a hard error — a template can never render half-filled.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .config import ConfigError, load_yaml, org_path

TOKEN = re.compile(r"\{\{\s*foundry\.([A-Za-z0-9_]+)\s*\}\}")
MANIFEST = "template.yaml"


@dataclass
class TemplateVariable:
    name: str
    description: str = ""
    default: Any = None
    required: bool = False


@dataclass
class Template:
    name: str
    path: Path
    description: str = ""
    variables: list[TemplateVariable] = field(default_factory=list)


def templates_dir(root: Path) -> Path:
    return root / "templates"


def list_templates(root: Path) -> list[Template]:
    found: list[Template] = []
    base = templates_dir(root)
    if not base.is_dir():
        return found
    for manifest in sorted(base.glob(f"*/{MANIFEST}")):
        found.append(load_template(manifest.parent))
    return found


def load_template(path: Path) -> Template:
    manifest_path = path / MANIFEST
    if not manifest_path.is_file():
        raise ConfigError(f"'{path.name}' is not a template (missing {MANIFEST})")
    manifest = load_yaml(manifest_path)
    variables = [
        TemplateVariable(
            name=str(v["name"]),
            description=str(v.get("description", "")),
            default=v.get("default"),
            required=bool(v.get("required", False)),
        )
        for v in manifest.get("variables", [])
    ]
    return Template(
        name=str(manifest.get("name", path.name)),
        path=path,
        description=str(manifest.get("description", "")),
        variables=variables,
    )


def builtin_variables(root: Path, dest: Path) -> dict[str, str]:
    import datetime

    values: dict[str, str] = {
        "name": dest.name,
        "year": str(datetime.date.today().year),
    }
    org_file = org_path(root)
    if org_file.is_file():
        meta = load_yaml(org_file).get("metadata", {})
        values["org"] = str(meta.get("name", ""))
        values["org_domain"] = str(meta.get("domain", ""))
        values["org_repository"] = str(meta.get("repository", ""))
    return values


def resolve_variables(
    template: Template, provided: dict[str, str], builtins: dict[str, str]
) -> dict[str, str]:
    values = dict(builtins)
    missing: list[str] = []
    for var in template.variables:
        if var.name in provided:
            values[var.name] = provided[var.name]
        elif var.default is not None:
            values[var.name] = str(var.default)
        elif var.name in values:
            pass  # satisfied by a builtin (e.g. `name`)
        elif var.required:
            missing.append(var.name)
        else:
            values[var.name] = ""
    values.update(provided)  # extra --var flags always win
    if missing:
        raise ConfigError(
            "missing required template variables: "
            + ", ".join(missing)
            + "  (pass with --var name=value)"
        )
    return values


def _render_text(text: str, values: dict[str, str], location: str) -> str:
    unknown: set[str] = set()

    def substitute(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in values:
            unknown.add(key)
            return match.group(0)
        return values[key]

    rendered = TOKEN.sub(substitute, text)
    if unknown:
        raise ConfigError(f"{location}: unknown template variable(s): {', '.join(sorted(unknown))}")
    return rendered


def _render_path(relative: Path, values: dict[str, str]) -> Path:
    parts = []
    for part in relative.parts:
        for key, value in values.items():
            part = part.replace(f"__{key}__", value)
        parts.append(part)
    return Path(*parts)


def render(
    root: Path,
    template_name: str,
    dest: Path,
    provided: dict[str, str],
    force: bool = False,
) -> list[Path]:
    """Render a template into *dest*. Returns the list of written files."""
    template = load_template(templates_dir(root) / template_name)
    values = resolve_variables(template, provided, builtin_variables(root, dest))

    if dest.exists() and any(dest.iterdir()) and not force:
        raise ConfigError(f"destination '{dest}' exists and is not empty (use --force)")
    dest.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for source in sorted(template.path.rglob("*")):
        relative = source.relative_to(template.path)
        if relative.name == MANIFEST:
            continue
        target = dest / _render_path(relative, values)
        if source.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            text = source.read_text(encoding="utf-8")
        except UnicodeDecodeError:  # binary asset — copy through untouched
            shutil.copy2(source, target)
        else:
            target.write_text(_render_text(text, values, str(relative)), encoding="utf-8")
            shutil.copymode(source, target)
        written.append(target)
    return written


def describe(template: Template) -> str:
    lines = [f"{template.name} — {template.description}".rstrip(" —")]
    if template.variables:
        lines.append("  variables:")
        for var in template.variables:
            default = f" (default: {var.default})" if var.default is not None else ""
            required = " [required]" if var.required else ""
            lines.append(f"    --var {var.name}=…{required}{default}  {var.description}")
    return "\n".join(lines)


def dump_manifest(template: Template) -> str:
    return yaml.safe_dump(
        {
            "name": template.name,
            "description": template.description,
            "variables": [v.__dict__ for v in template.variables],
        },
        sort_keys=False,
    )
