"""Unit tests for the Foundry CLI core.

These build tiny hermetic workspaces in tmp_path rather than depending on the
repository's own config, so behaviour is pinned independently of the demo
content.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from foundry_cli import render, scaffold, stack, validate
from foundry_cli.config import ConfigError, find_root, name_for, render_context

ORG = """\
apiVersion: foundry/v1
kind: Organization
metadata: {name: acme, domain: acme.test}
spec:
  cloud:
    defaultProvider: digitalocean
    providers:
      digitalocean: {region: nyc3}
      aws: {region: us-east-1}
  naming: {pattern: "{org}-{project}-{environment}-{component}", delimiter: "-"}
  labels: {managed-by: foundry, tier-default: standard}
  network: {cidr: "10.0.0.0/8"}
  state: {backend: s3, bucket: acme-tfstate, region: nyc3,
          endpoint: "https://nyc3.digitaloceanspaces.com"}
"""

PROJECT = """\
apiVersion: foundry/v1
kind: Project
metadata: {name: app}
spec:
  stacks: [network]
  labels: {team: platform}
"""

ENV_DEV = """\
apiVersion: foundry/v1
kind: Environment
metadata: {name: dev}
spec:
  tier: nonproduction
  cloud: {region: sfo3}
  network: {cidr: "10.20.0.0/16"}
  labels: {team: dev-overrides-project}
"""

ENV_PROD = """\
apiVersion: foundry/v1
kind: Environment
metadata: {name: prod}
spec:
  tier: production
  network: {cidr: "10.40.0.0/16"}
"""


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    config = tmp_path / "config"
    (config / "projects").mkdir(parents=True)
    (config / "environments").mkdir(parents=True)
    (config / "foundry.yaml").write_text(ORG)
    (config / "projects" / "app.yaml").write_text(PROJECT)
    (config / "environments" / "dev.yaml").write_text(ENV_DEV)
    (config / "environments" / "prod.yaml").write_text(ENV_PROD)
    (tmp_path / "stacks" / "network").mkdir(parents=True)
    (tmp_path / "stacks" / "network" / "main.tf").write_text(
        'variable "foundry_context" { type = any }\n'
    )
    return tmp_path


# --------------------------------------------------------------------------- #
# Configuration merge, precedence, provenance
# --------------------------------------------------------------------------- #
def test_find_root_walks_upward(workspace: Path) -> None:
    nested = workspace / "stacks" / "network"
    assert find_root(nested) == workspace


def test_precedence_env_overrides_project_overrides_org(workspace: Path) -> None:
    context, origins = render_context(workspace, "app", "dev")
    labels = context["computed"]["labels"]
    assert labels["team"] == "dev-overrides-project"
    assert labels["tier-default"] == "standard"  # inherited from org
    assert labels["project"] == "app" and labels["environment"] == "dev"
    assert origins["labels.team"].endswith("environments/dev.yaml")
    assert origins["labels.tier-default"].endswith("foundry.yaml")


def test_region_resolution_env_beats_provider_default(workspace: Path) -> None:
    dev, _ = render_context(workspace, "app", "dev")
    prod, _ = render_context(workspace, "app", "prod")
    assert dev["computed"]["region"] == "sfo3"  # env override
    assert prod["computed"]["region"] == "nyc3"  # provider default


def test_local_override_wins(workspace: Path) -> None:
    (workspace / "foundry.local.yaml").write_text("spec:\n  cloud: {region: ams3}\n")
    context, origins = render_context(workspace, "app", "dev")
    assert context["computed"]["region"] == "ams3"
    assert origins["cloud.region"] == "foundry.local.yaml"


def test_naming_pattern(workspace: Path) -> None:
    context, _ = render_context(workspace, "app", "dev")
    assert context["computed"]["name_prefix"] == "acme-app-dev"
    assert name_for(context["spec"], "acme", "app", "dev", "vpc") == "acme-app-dev-vpc"


def test_unknown_project_raises(workspace: Path) -> None:
    with pytest.raises(ConfigError, match="unknown project"):
        render_context(workspace, "ghost", "dev")


# --------------------------------------------------------------------------- #
# Exports
# --------------------------------------------------------------------------- #
def test_tfvars_export_shape(workspace: Path) -> None:
    context, _ = render_context(workspace, "app", "dev")
    payload = json.loads(render.to_tfvars(context))
    assert payload["foundry_context"]["computed"]["provider"] == "digitalocean"
    assert payload["foundry_context"]["spec"]["network"]["cidr"] == "10.20.0.0/16"


def test_dotenv_export(workspace: Path) -> None:
    context, _ = render_context(workspace, "app", "dev")
    out = render.to_dotenv(context)
    assert "FOUNDRY_NAME_PREFIX=acme-app-dev\n" in out
    assert "FOUNDRY_PROVIDER=digitalocean\n" in out


def test_backend_export_spaces_endpoint(workspace: Path) -> None:
    context, _ = render_context(workspace, "app", "dev")
    out = render.to_backend(context, "network")
    assert 'key = "acme/app/dev/network.tfstate"' in out
    assert 'bucket = "acme-tfstate"' in out
    assert "use_path_style" in out  # Spaces/MinIO via the s3 backend


# --------------------------------------------------------------------------- #
# Validation invariants
# --------------------------------------------------------------------------- #
def test_validate_flags_cidr_overlap_and_plaintext_secret(workspace: Path) -> None:
    (workspace / "config" / "environments" / "qa.yaml").write_text(
        "apiVersion: foundry/v1\nkind: Environment\nmetadata: {name: qa}\n"
        "spec: {network: {cidr: '10.20.0.0/16'}}\n"
    )
    secrets = workspace / "config" / "secrets"
    secrets.mkdir()
    (secrets / "oops.yaml").write_text("password: hunter2\n")
    findings = validate.validate_workspace(workspace)
    messages = "\n".join(f.message for f in findings if f.severity == "error")
    assert "overlaps" in messages
    assert "plaintext YAML" in messages


def test_validate_clean_workspace_has_no_errors(workspace: Path) -> None:
    findings = validate.validate_workspace(workspace)
    assert [f for f in findings if f.severity == "error"] == []


# --------------------------------------------------------------------------- #
# Scaffolder
# --------------------------------------------------------------------------- #
def test_scaffold_renders_tokens_paths_and_preserves_actions_syntax(workspace: Path) -> None:
    tpl = workspace / "templates" / "svc"
    (tpl / "__service__").mkdir(parents=True)
    (tpl / "template.yaml").write_text(
        "name: svc\ndescription: test\nvariables:\n"
        "  - {name: service, required: true}\n  - {name: port, default: 8080}\n"
    )
    (tpl / "__service__" / "app.txt").write_text(
        "svc={{ foundry.service }} port={{foundry.port}} org={{ foundry.org }}\n"
        "gha=${{ github.ref }}\n"
    )
    dest = workspace / "out" / "shop"
    written = scaffold.render(workspace, "svc", dest, {"service": "shop"})
    rendered = (dest / "shop" / "app.txt").read_text()
    assert "svc=shop port=8080 org=acme" in rendered
    assert "${{ github.ref }}" in rendered  # Actions expressions untouched
    assert len(written) == 1


def test_scaffold_missing_required_variable_fails(workspace: Path) -> None:
    tpl = workspace / "templates" / "svc"
    tpl.mkdir(parents=True)
    (tpl / "template.yaml").write_text(
        "name: svc\nvariables: [{name: service, required: true}]\n"
    )
    (tpl / "f.txt").write_text("x")
    with pytest.raises(ConfigError, match="missing required"):
        scaffold.render(workspace, "svc", workspace / "out2", {})


def test_scaffold_unknown_token_fails(workspace: Path) -> None:
    tpl = workspace / "templates" / "svc"
    tpl.mkdir(parents=True)
    (tpl / "template.yaml").write_text("name: svc\n")
    (tpl / "f.txt").write_text("{{ foundry.nope }}")
    with pytest.raises(ConfigError, match="unknown template variable"):
        scaffold.render(workspace, "svc", workspace / "out3", {})


# --------------------------------------------------------------------------- #
# Stack runner
# --------------------------------------------------------------------------- #
def test_stack_dry_run_generates_inputs_and_commands(workspace: Path) -> None:
    run = stack.run(workspace, "plan", "app", "dev", "network", dry_run=True)
    generated = run.workdir / ".foundry"
    assert (generated / "stack.tfvars.json").is_file()
    assert (generated / "backend.hcl").is_file()
    flat = [" ".join(c) for c in run.commands]
    assert any("init" in c and "-backend-config" in c for c in flat)
    assert any(
        c.endswith("plan -input=false -var-file .foundry/stack.tfvars.json") for c in flat
    )


def test_stack_prod_requires_allow_prod(workspace: Path) -> None:
    with pytest.raises(ConfigError, match="--allow-prod"):
        stack.run(workspace, "apply", "app", "prod", "network", dry_run=True)
    run = stack.run(workspace, "apply", "app", "prod", "network", dry_run=True, allow_prod=True)
    assert run.commands
