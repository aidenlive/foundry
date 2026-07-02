# CI/CD

All automation lives in `.github/workflows/`; everything a workflow does can
be reproduced locally with `make` or `foundry` commands — CI is a convenience
layer, not a magic one.

## ci.yml — every push and PR

ruff → pytest → yamllint → HCL parse gate (`scripts/check_hcl.py`) →
`foundry validate` → `mkdocs build --strict`, plus a separate
`tofu fmt -check` job. Green CI means: code lints, tests pass, config is
valid, every `.tf` parses, docs build with no broken nav.

## terraform-reusable.yml — the stack pipeline

A `workflow_call` workflow: project workflows stay tiny.

```yaml
jobs:
  network-prod:
    uses: ./.github/workflows/terraform-reusable.yml
    with: {project: demo, environment: prod, stack: network, action: apply}
    secrets: inherit
```

Key property: the job binds to the **GitHub environment named after the
Foundry environment**. Configure required reviewers on `staging`/`prod`
environments in repo settings and every apply pauses for human approval —
provider credentials are environment-scoped secrets, so dev tokens can't
touch prod.

Recommended flow: `action: plan` on pull requests, `action: apply` on merge
to `main` (or manual dispatch), one job per stack in dependency order via
`needs:`.

## drift.yml — nightly

Plans every production stack with `-detailed-exitcode`; a non-empty plan
opens (or comments on) an issue labeled `drift`/`ops` linking the run.
Add stacks to the matrix as they reach production. Drift issues are triaged
like bugs: reconcile config to reality or reality to config — never ignore.

## docs.yml and release.yml

Docs: build with `--strict` and deploy to GitHub Pages on changes to
`docs/`/`mkdocs.yml`. Release: pushing a `v*` tag builds the CLI
distributions and publishes a GitHub release with generated notes.

## Supply-chain hygiene

Dependabot (pip + actions, weekly), CODEOWNERS on `modules/`, `config/`, and
`.github/`, `gitleaks` in pre-commit, and minimal workflow `permissions`
blocks throughout.
