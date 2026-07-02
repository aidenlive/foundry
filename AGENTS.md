# Foundry — Agent Guide

Machine-first orientation for AI coding agents working in this repository.
Humans: start at README.md or the docs site instead.

## What this repository is

A cloud-agnostic infrastructure toolkit. Layered YAML configuration under
`config/` is the single source of truth; the `foundry` CLI renders it into
Terraform/OpenTofu inputs, state backends, env files, scaffolds, and docs.

## Ground truth commands

```bash
./scripts/bootstrap.sh && source .venv/bin/activate   # one-time setup
foundry context --format json    # machine-readable repo map (layout, commands)
foundry validate                 # schemas + invariants; run after config edits
foundry config render -p demo -e dev        # fully merged context
foundry config get -p demo -e dev <path>    # one value + originating file
foundry stack plan -p <proj> -e <env> -s <stack> --dry-run   # never applies
make validate                    # full local gate (lint, tests, HCL, docs)
```

## Rules that will save you

1. **Never hand-edit rendered artifacts** (`.foundry/`, `site/`,
   `*.tfvars.json`). Change `config/` and re-render.
2. **Config precedence** is org < project < environment < `foundry.local.yaml`.
   Maps deep-merge; scalars and lists replace. `foundry config get` shows the
   winning file — trust it over grep.
3. **Module contracts are frozen per capability.** Changing a variable/output
   means updating all four provider implementations + the capability README.
4. **Do not weaken security defaults** (encryption, deny-by-default ingress,
   IMDSv2, private buckets, `--allow-prod` guard). Tightening is fine.
5. **Secrets:** only `config/secrets/*.enc.yaml` via `foundry secrets`;
   `foundry validate` fails on plaintext YAML there. Never print decrypted
   values into files or logs.
6. **Templates** use `{{ foundry.var }}` tokens; GitHub Actions `${{ … }}` is
   untouched. Unknown `foundry.*` tokens fail the render on purpose.
7. **Tests and docs gate merges:** pytest under `cli/tests`,
   `scripts/check_hcl.py` for HCL, `mkdocs build --strict` for docs — keep
   nav in `mkdocs.yml` in sync with files in `docs/`.

## Where things live

| Need                        | Location                                   |
| --------------------------- | ------------------------------------------ |
| Org/project/env config      | `config/…yaml` (schemas in `config/schema`) |
| CLI source + tests          | `cli/src/foundry_cli`, `cli/tests`         |
| Module contracts            | `modules/<capability>/<component>/README.md` |
| Deployable roots            | `stacks/`                                  |
| Scaffolds                   | `templates/` (manifest: `template.yaml`)   |
| Operational procedure       | `ops/runbooks`, `ops/checklists`           |
| Prose docs                  | `docs/` (`mkdocs.yml` nav)                 |
