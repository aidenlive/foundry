"""Foundry command-line interface.

One binary, one mental model: everything reads the merged configuration
context and everything can be previewed before it mutates anything.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from . import __version__, doctor, render, scaffold, secrets, stack, validate
from . import context as ctxmod
from .config import (
    ConfigError,
    find_root,
    get_path,
    list_environments,
    list_projects,
    render_context,
)
from .util import eprint, parse_var_flags

STARTER_ORG = """\
apiVersion: foundry/v1
kind: Organization
metadata:
  name: {org}
spec:
  cloud:
    defaultProvider: digitalocean
    providers:
      digitalocean: {{ region: nyc3 }}
  naming:
    pattern: "{{org}}-{{project}}-{{environment}}-{{component}}"
    delimiter: "-"
  labels:
    managed-by: foundry
    org: {org}
  network:
    cidr: "10.0.0.0/8"
  security:
    encryptionAtRest: required
    publicIngressDefault: deny
    ssh: {{ port: 22, allowedCidrs: [] }}
  state:
    backend: local
"""

STARTER_ENV = """\
apiVersion: foundry/v1
kind: Environment
metadata:
  name: {name}
spec:
  tier: {tier}
  network:
    cidr: "{cidr}"
  labels:
    environment: {name}
"""


def _root(args: argparse.Namespace) -> Path:
    return find_root(Path(args.chdir) if args.chdir else None)


# --------------------------------------------------------------------------- #
# Command handlers
# --------------------------------------------------------------------------- #
def cmd_init(args: argparse.Namespace) -> int:
    base = Path(args.chdir or ".").resolve()
    config_dir = base / "config"
    if (config_dir / "foundry.yaml").exists():
        eprint(f"foundry: {config_dir}/foundry.yaml already exists — nothing to do")
        return 1
    (config_dir / "projects").mkdir(parents=True, exist_ok=True)
    (config_dir / "environments").mkdir(parents=True, exist_ok=True)
    (config_dir / "foundry.yaml").write_text(STARTER_ORG.format(org=args.org), encoding="utf-8")
    for name, tier, cidr in (("dev", "nonproduction", "10.20.0.0/16"),
                             ("prod", "production", "10.40.0.0/16")):
        (config_dir / "environments" / f"{name}.yaml").write_text(
            STARTER_ENV.format(name=name, tier=tier, cidr=cidr), encoding="utf-8"
        )
    print(f"Initialized Foundry workspace for org '{args.org}' in {base}")
    print("Next: add a project under config/projects/, then `foundry validate`.")
    print("Docs: https://standardcompute.github.io/foundry/getting-started/quickstart/")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    findings = validate.validate_workspace(_root(args))
    errors = [f for f in findings if f.severity == "error"]
    for finding in findings:
        eprint(str(finding))
    if errors:
        warnings = len(findings) - len(errors)
        eprint(f"foundry validate: {len(errors)} error(s), {warnings} warning(s)")
        return 1
    print(f"foundry validate: OK ({len(findings)} warning(s))")
    return 0


def cmd_config(args: argparse.Namespace) -> int:
    root = _root(args)
    if args.config_command == "projects":
        print("\n".join(list_projects(root)))
        return 0
    if args.config_command == "environments":
        print("\n".join(list_environments(root)))
        return 0

    context, origins = render_context(root, args.project, args.environment)
    if args.config_command == "render":
        sys.stdout.write(render.export(context, args.format))
        return 0
    if args.config_command == "export":
        output = render.export(context, args.format, stack=args.stack)
        if args.out:
            Path(args.out).write_text(output, encoding="utf-8")
            print(f"wrote {args.out}")
        else:
            sys.stdout.write(output)
        return 0
    if args.config_command == "get":
        origin_key: str | None
        try:  # full-context path first (e.g. computed.provider, spec.labels.team)
            value = get_path(context, args.path)
            origin_key = args.path.removeprefix("spec.") if args.path.startswith("spec.") else None
        except KeyError:
            try:  # bare spec path as a convenience (e.g. kubernetes.minNodes)
                value = get_path(context["spec"], args.path)
                origin_key = args.path
            except KeyError:
                eprint(f"foundry: no such key '{args.path}'")
                return 1
        origin = "(computed)"
        if origin_key is not None:
            origin = origins.get(origin_key) or next(
                (origins[k] for k in sorted(origins) if k.startswith(origin_key + ".")),
                "(computed)",
            )
        print(render.to_yaml({args.path: value}).rstrip())
        print(f"# source: {origin}")
        return 0
    raise AssertionError("unreachable")


def cmd_new(args: argparse.Namespace) -> int:
    root = _root(args)
    if args.list:
        for template in scaffold.list_templates(root):
            print(scaffold.describe(template))
            print()
        return 0
    if not args.template or not args.dest:
        eprint("foundry new: TEMPLATE and DEST are required (or use --list)")
        return 2
    written = scaffold.render(
        root, args.template, Path(args.dest), parse_var_flags(args.var), force=args.force
    )
    print(f"rendered template '{args.template}' → {args.dest} ({len(written)} files)")
    return 0


def cmd_stack(args: argparse.Namespace) -> int:
    run = stack.run(
        _root(args),
        action=args.action,
        project=args.project,
        environment=args.environment,
        stack=args.stack,
        extra=args.extra,
        dry_run=args.dry_run,
        allow_prod=args.allow_prod,
    )
    if args.dry_run:
        sys.stdout.write(stack.format_dry_run(run))
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    checks = doctor.run_checks(_root(args))
    table, healthy = doctor.report(checks)
    print("foundry doctor — toolchain\n")
    print(table)
    if not healthy and args.strict:
        return 1
    return 0


def cmd_context(args: argparse.Namespace) -> int:
    output = ctxmod.render(_root(args), args.format)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(output)
    return 0


def cmd_secrets(args: argparse.Namespace) -> int:
    root = _root(args)
    if args.secrets_command == "init":
        print(secrets.init(root))
        return 0
    handler = {"edit": secrets.edit, "encrypt": secrets.encrypt, "decrypt": secrets.decrypt}
    return handler[args.secrets_command](root, args.path)


def cmd_docs(args: argparse.Namespace) -> int:
    root = _root(args)
    if not shutil.which("mkdocs"):
        eprint("foundry docs: mkdocs not found — run `make setup` (installs mkdocs-material)")
        return 1
    serve = args.docs_command == "serve"
    command = ["mkdocs", "serve"] if serve else ["mkdocs", "build", "--strict"]
    return subprocess.run(command, cwd=root).returncode  # noqa: S603 - user-invoked tool


# --------------------------------------------------------------------------- #
# Parser
# --------------------------------------------------------------------------- #
def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="foundry",
        description="Foundry — a cloud-agnostic infrastructure toolkit (Standard Compute Org.)",
    )
    parser.add_argument("-C", "--chdir", metavar="DIR", help="operate as if started in DIR")
    parser.add_argument("--version", action="version", version=f"foundry {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="initialize a new Foundry workspace in the current directory")
    p.add_argument("--org", required=True, help="organization name (DNS-safe)")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("validate", help="validate config/ against schemas and invariants")
    p.set_defaults(func=cmd_validate)

    p = sub.add_parser("config", help="render, query, and export merged configuration")
    csub = p.add_subparsers(dest="config_command", required=True)
    for name in ("render", "export"):
        cp = csub.add_parser(name, help=f"{name} the merged context")
        cp.add_argument("-p", "--project", required=True)
        cp.add_argument("-e", "--environment", required=True)
        cp.add_argument(
            "-f", "--format", default="yaml" if name == "render" else "json",
            choices=render.FORMATS,
        )
        cp.add_argument("--stack", default="stack", help="stack name (backend format only)")
        cp.add_argument("-o", "--out", help="write to a file instead of stdout")
    cp = csub.add_parser("get", help="show one value and the file that set it")
    cp.add_argument("path", help="dotted path, e.g. spec.kubernetes.minNodes")
    cp.add_argument("-p", "--project", required=True)
    cp.add_argument("-e", "--environment", required=True)
    csub.add_parser("projects", help="list configured projects")
    csub.add_parser("environments", help="list configured environments")
    p.set_defaults(func=cmd_config)

    p = sub.add_parser("new", help="scaffold from a template in templates/")
    p.add_argument("template", nargs="?", help="template name (see --list)")
    p.add_argument("dest", nargs="?", help="destination directory")
    p.add_argument("--var", action="append", default=[], metavar="NAME=VALUE")
    p.add_argument("--force", action="store_true", help="render into a non-empty directory")
    p.add_argument("--list", action="store_true", help="list available templates")
    p.set_defaults(func=cmd_new)

    p = sub.add_parser("stack", help="run OpenTofu/Terraform on a stack with generated inputs")
    p.add_argument("action", choices=stack.ACTIONS)
    p.add_argument("-p", "--project", required=True)
    p.add_argument("-e", "--environment", required=True)
    p.add_argument("-s", "--stack", required=True)
    p.add_argument("--dry-run", action="store_true", help="print commands without executing")
    p.add_argument("--allow-prod", action="store_true",
                   help="permit apply/destroy on tier: production environments")
    p.add_argument("extra", nargs="*",
                   help="arguments after -- pass through to the engine")
    p.set_defaults(func=cmd_stack)

    p = sub.add_parser("doctor", help="check the local toolchain")
    p.add_argument("--strict", action="store_true", help="exit non-zero if no IaC engine is found")
    p.set_defaults(func=cmd_doctor)

    p = sub.add_parser("context", help="emit AI/agent-friendly repository context")
    p.add_argument("-f", "--format", default="markdown", choices=("markdown", "json"))
    p.add_argument("-o", "--out", help="write to a file instead of stdout")
    p.set_defaults(func=cmd_context)

    p = sub.add_parser("secrets", help="manage sops+age encrypted secrets")
    ssub = p.add_subparsers(dest="secrets_command", required=True)
    ssub.add_parser("init", help="verify sops/age and print setup steps")
    for name in ("edit", "encrypt", "decrypt"):
        sp = ssub.add_parser(name)
        sp.add_argument("path")
    p.set_defaults(func=cmd_secrets)

    p = sub.add_parser("docs", help="build or serve the documentation site")
    p.add_argument("docs_command", nargs="?", default="build", choices=("build", "serve"))
    p.set_defaults(func=cmd_docs)

    return parser


def main(argv: list[str] | None = None) -> int:
    tokens = list(sys.argv[1:] if argv is None else argv)
    passthrough: list[str] = []
    if "--" in tokens:
        split = tokens.index("--")
        tokens, passthrough = tokens[:split], tokens[split + 1 :]
    args = build_parser().parse_args(tokens)
    if passthrough:
        if hasattr(args, "extra"):
            args.extra = [*args.extra, *passthrough]
        else:
            eprint("foundry: arguments after '--' are only supported by 'foundry stack'")
            return 2
    try:
        return args.func(args)
    except ConfigError as exc:
        eprint(f"foundry: {exc}")
        return 1
    except ValueError as exc:
        eprint(f"foundry: {exc}")
        return 2
    except KeyboardInterrupt:
        eprint("foundry: interrupted")
        return 130


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
