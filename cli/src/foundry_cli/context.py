"""`foundry context` — emit an AI/agent-friendly snapshot of the workspace.

Coding agents and humans alike get one command that answers: what is this
repository, how is it laid out, what are the golden commands, and what
invariants must hold. The same data backs AGENTS.md and docs/llms.txt.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from . import __version__
from .config import list_environments, list_projects, load_yaml, org_path
from .scaffold import list_templates

LAYOUT = {
    "config/": "Source of truth: org/project/environment configuration + JSON Schemas.",
    "cli/": "The `foundry` CLI (Python). Everything else is driven through it.",
    "modules/": "Cloud-agnostic IaC modules: one contract per capability, per-provider impls.",
    "stacks/": "Deployable compositions of modules; consume config via var.foundry_context.",
    "templates/": "Project scaffolds rendered by `foundry new` ({{ foundry.* }} tokens).",
    ".github/": "CI/CD: checks, reusable Terraform plan/apply, drift detection, docs deploy.",
    "ops/": "Operational runbooks and production-readiness checklists.",
    "docs/": "MkDocs source for the documentation site (humans + llms.txt for agents).",
    "scripts/": "Bootstrap and repository hygiene scripts.",
}

COMMANDS = {
    "make setup": "Create .venv and install the CLI with dev extras.",
    "make test": "Run the CLI unit tests.",
    "make lint": "ruff + yamllint + HCL parse check.",
    "foundry validate": "Schema + invariant checks over config/.",
    "foundry config render -p <project> -e <env>": "Show the merged configuration context.",
    "foundry config get <dotted.path> -p <project> -e <env>": "Show a value and which file set it.",
    "foundry new <template> <dest>": "Scaffold from templates/.",
    "foundry stack plan -p <proj> -e <env> -s <stack>": "Plan with generated tfvars/backend.",
    "foundry doctor": "Check local toolchain versions.",
    "make docs": "Build the documentation site (mkdocs --strict).",
}

CONVENTIONS = [
    "config/ is the only place settings live; stacks and templates consume the rendered context.",
    "Precedence: org < project < environment < local. Maps merge; lists/scalars replace.",
    "Module contract: same variables/outputs across providers; provider chosen by path.",
    "Names follow spec.naming.pattern; labels always include org/project/environment/managed-by.",
    "No plaintext secrets in git — sops+age under config/secrets/, verified by `foundry validate`.",
    "Production environments (tier: production) require --allow-prod for apply/destroy.",
    "Every change: run `foundry validate` and `make test`; update docs/ and CHANGELOG.md.",
]


def build(root: Path) -> dict[str, Any]:
    org = load_yaml(org_path(root))
    meta = org.get("metadata", {})
    spec = org.get("spec", {})
    return {
        "name": "Foundry",
        "version": __version__,
        "summary": (
            "Open-source (MIT), cloud-agnostic infrastructure toolkit: centralized "
            "configuration, reusable IaC modules, a CLI, project templates, GitHub "
            "automation, runbooks, and docs that work as one platform."
        ),
        "organization": {
            "name": meta.get("name"),
            "domain": meta.get("domain"),
            "repository": meta.get("repository"),
        },
        "configuration": {
            "defaultProvider": spec.get("cloud", {}).get("defaultProvider"),
            "projects": list_projects(root),
            "environments": list_environments(root),
            "precedence": [
                "config/foundry.yaml",
                "config/projects/*",
                "config/environments/*",
                "foundry.local.yaml",
            ],
        },
        "templates": [t.name for t in list_templates(root)],
        "layout": {k: v for k, v in LAYOUT.items() if (root / k).exists()},
        "commands": COMMANDS,
        "conventions": CONVENTIONS,
        "entrypoints": {
            "humans": "docs/index.md (site: mkdocs.yml)",
            "agents": ["AGENTS.md", "docs/llms.txt", "foundry context --format json"],
        },
    }


def to_markdown(data: dict[str, Any]) -> str:
    lines = [f"# {data['name']} {data['version']} — repository context", "", data["summary"], ""]
    lines += ["## Layout", ""]
    lines += [f"- `{path}` — {desc}" for path, desc in data["layout"].items()]
    lines += ["", "## Golden commands", ""]
    lines += [f"- `{cmd}` — {desc}" for cmd, desc in data["commands"].items()]
    lines += ["", "## Conventions", ""]
    lines += [f"- {rule}" for rule in data["conventions"]]
    cfg = data["configuration"]
    lines += [
        "",
        "## Configuration",
        "",
        f"- default provider: `{cfg['defaultProvider']}`",
        f"- projects: {', '.join(cfg['projects']) or '(none)'}",
        f"- environments: {', '.join(cfg['environments']) or '(none)'}",
        f"- precedence: {' < '.join(cfg['precedence'])}",
    ]
    return "\n".join(lines) + "\n"


def render(root: Path, fmt: str) -> str:
    data = build(root)
    if fmt == "json":
        return json.dumps(data, indent=2) + "\n"
    return to_markdown(data)
