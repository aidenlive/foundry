"""`foundry doctor` — verify the local toolchain against spec.toolchain."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from .config import load_yaml, org_path

BINARIES = {
    "opentofu": "tofu",
    "terraform": "terraform",
    "kubectl": "kubectl",
    "helm": "helm",
    "sops": "sops",
    "age": "age",
    "git": "git",
    "python": sys.executable,
}
VERSION_RE = re.compile(r"(\d+\.\d+(?:\.\d+)?)")


@dataclass
class Check:
    tool: str
    required: str
    found: str | None  # version string, or None when the binary is missing


def _detect_version(binary: str) -> str | None:
    path = shutil.which(binary)
    if not path:
        return None
    try:
        out = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=10)
        first = (out.stdout or out.stderr).splitlines()
        text = first[0] if first else ""
    except (OSError, subprocess.TimeoutExpired):
        return "installed"
    match = VERSION_RE.search(text)
    return match.group(1) if match else "installed"


def run_checks(root: Path) -> list[Check]:
    toolchain = load_yaml(org_path(root)).get("spec", {}).get("toolchain", {})
    tools = dict(toolchain)
    tools.setdefault("git", ">=2.30")
    return [
        Check(tool=tool, required=str(required), found=_detect_version(BINARIES.get(tool, tool)))
        for tool, required in sorted(tools.items())
    ]


def report(checks: list[Check]) -> tuple[str, bool]:
    """Render the table; healthy=False when no IaC engine is available."""
    core = {"python", "git", "opentofu", "terraform"}
    width = max(len(c.tool) for c in checks) + 2
    lines = []
    for c in checks:
        if c.found:
            mark = "ok"
        elif c.tool in core:
            mark = "MISSING"
        else:
            mark = "na"
        found = c.found or "-"
        note = "" if c.tool in core else "  (optional)"
        lines.append(
            f"  {mark:<9s}{c.tool:<{width}}wants {c.required:<10s} found {found}{note}"
        )
    by_tool = {c.tool: c.found for c in checks}
    healthy = bool(by_tool.get("opentofu") or by_tool.get("terraform"))
    if not healthy:
        lines.append("")
        lines.append("  no IaC engine found: install OpenTofu (preferred) or Terraform")
    return "\n".join(lines), healthy
