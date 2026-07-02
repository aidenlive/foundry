"""`foundry stack` — run OpenTofu/Terraform against a stack with the rendered
configuration context injected, so plans and applies are identical on a
laptop and in CI.

For every run Foundry writes two generated inputs into ``<stack>/.foundry/``
(git-ignored):

* ``stack.tfvars.json`` — the merged context, exposed to HCL as
  ``var.foundry_context``,
* ``backend.hcl``       — partial remote-state configuration derived from
  ``spec.state`` (only when a remote backend is configured).
"""

from __future__ import annotations

import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .config import ConfigError, render_context
from .render import to_backend, to_tfvars

ACTIONS = ("init", "plan", "apply", "destroy", "output", "validate")
GENERATED_DIR = ".foundry"


@dataclass
class StackRun:
    binary: str
    workdir: Path
    commands: list[list[str]]


def find_binary() -> str | None:
    for candidate in ("tofu", "terraform"):
        if shutil.which(candidate):
            return candidate
    return None


def resolve_stack_dir(root: Path, project: str, stack: str) -> Path:
    for candidate in (root / "stacks" / project / stack, root / "stacks" / stack):
        if candidate.is_dir():
            return candidate
    raise ConfigError(
        f"stack '{stack}' not found (looked in stacks/{project}/{stack} and stacks/{stack})"
    )


def prepare(root: Path, project: str, environment: str, stack: str) -> tuple[Path, dict[str, Any]]:
    """Render context and write the generated inputs into the stack dir."""
    context, _ = render_context(root, project, environment)
    workdir = resolve_stack_dir(root, project, stack)

    generated = workdir / GENERATED_DIR
    generated.mkdir(exist_ok=True)
    (generated / ".gitignore").write_text("*\n", encoding="utf-8")
    (generated / "stack.tfvars.json").write_text(to_tfvars(context), encoding="utf-8")

    backend = to_backend(context, stack)
    backend_file = generated / "backend.hcl"
    if backend.startswith("#") and "no remote backend" in backend:
        backend_file.unlink(missing_ok=True)
    else:
        backend_file.write_text(backend, encoding="utf-8")
    return workdir, context


def build_commands(binary: str, workdir: Path, action: str, extra: list[str]) -> list[list[str]]:
    backend_args = (
        ["-backend-config", f"{GENERATED_DIR}/backend.hcl"]
        if (workdir / GENERATED_DIR / "backend.hcl").is_file()
        else []
    )
    var_args = ["-var-file", f"{GENERATED_DIR}/stack.tfvars.json"]
    init = [binary, "init", "-input=false", *backend_args]

    if action == "init":
        return [init + extra]
    if action == "validate":
        return [init, [binary, "validate", *extra]]
    if action == "output":
        return [[binary, "output", *extra]]
    if action in ("plan", "apply", "destroy"):
        return [init, [binary, action, "-input=false", *var_args, *extra]]
    raise ConfigError(f"unknown action '{action}' (choose from: {', '.join(ACTIONS)})")


def run(
    root: Path,
    action: str,
    project: str,
    environment: str,
    stack: str,
    extra: list[str] | None = None,
    dry_run: bool = False,
    allow_prod: bool = False,
) -> StackRun:
    extra = [arg for arg in (extra or []) if arg != "--"]
    workdir, context = prepare(root, project, environment, stack)

    if (
        context["computed"]["tier"] == "production"
        and action in ("apply", "destroy")
        and not allow_prod
    ):
        raise ConfigError(
            f"'{environment}' is a production-tier environment; re-run with --allow-prod "
            "to confirm a mutating action (CI applies should come from a protected branch)"
        )

    binary = find_binary() or "tofu"
    commands = build_commands(binary, workdir, action, extra)
    result = StackRun(binary=binary, workdir=workdir, commands=commands)

    if dry_run:
        return result
    if not shutil.which(binary):
        raise ConfigError(
            "neither 'tofu' (OpenTofu) nor 'terraform' found on PATH — "
            "install one, or use --dry-run to inspect the commands"
        )
    for command in commands:
        completed = subprocess.run(command, cwd=workdir)  # noqa: S603 - user-invoked tool
        if completed.returncode != 0:
            raise SystemExit(completed.returncode)
    return result


def format_dry_run(run_: StackRun) -> str:
    lines = [f"# workdir: {run_.workdir}"]
    lines += ["$ " + " ".join(cmd) for cmd in run_.commands]
    return "\n".join(lines) + "\n"
