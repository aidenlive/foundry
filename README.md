# Foundry

**Cloud-agnostic infrastructure toolkit by [Standard Compute Org](https://standardcompute.org).**
Version-controlled configuration in, reproducible infrastructure out — on
DigitalOcean, AWS, GCP, or Azure, from solo founder to multi-team platform.

[![CI](https://github.com/standardcompute/foundry/actions/workflows/ci.yml/badge.svg)](https://github.com/standardcompute/foundry/actions/workflows/ci.yml)
[![Docs](https://github.com/standardcompute/foundry/actions/workflows/docs.yml/badge.svg)](https://standardcompute.github.io/foundry)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Why

Most infrastructure repositories rot the same way: values scattered across
tfvars, CI variables, and tribal memory; modules welded to one provider;
environments that drift apart. Foundry inverts that:

- **Config is the source of truth.** Org → project → environment YAML layers
  with explicit precedence; everything else (Terraform inputs, state backends,
  env files, names, labels) is *rendered* from it.
- **Contracts over providers.** Each capability (`network/vpc`,
  `kubernetes/cluster`, …) has one interface and four interchangeable
  implementations. Moving clouds is a config change and one `source` line.
- **Secure and boring by default.** Encryption at rest, deny-by-default
  ingress, IMDSv2, sops-encrypted secrets, prod guarded by `--allow-prod`
  and CI environment reviews.

## Quickstart

```bash
git clone https://github.com/standardcompute/foundry && cd foundry
./scripts/bootstrap.sh && source .venv/bin/activate

foundry validate                                  # schema + invariants
foundry config render -p demo -e dev              # the merged truth
foundry config get -p demo -e prod kubernetes     # one value + its source file
foundry stack plan -p demo -e dev -s network --dry-run
foundry new service ./services/shop --var service_name=shop
```

Point `spec.state` in `config/foundry.yaml` at a bucket, export provider
credentials, drop the `--dry-run`, and you have a VPC.

## Repository layout

```
config/       Organization, projects, environments, schemas, encrypted secrets
cli/          `foundry` — render, validate, scaffold, run stacks, doctor, docs
modules/      Cloud-agnostic contracts × {aws, gcp, azure, digitalocean}
stacks/       Deployable roots (demo: DigitalOcean network + DOKS platform)
templates/    `foundry new` scaffolds: service, terraform-stack, static-site
ops/          Runbooks and checklists for humans at 3 a.m.
docs/         MkDocs site (humans) + llms.txt and AGENTS.md (agents)
.github/      CI, docs deploy, releases, reusable stack pipeline, drift watch
```

## Documentation

Full docs live at **[standardcompute.github.io/foundry](https://standardcompute.github.io/foundry)**
(or `make docs-serve` locally). AI agents: start with [AGENTS.md](AGENTS.md),
`docs/llms.txt`, or `foundry context --format json`.

## Contributing & license

See [CONTRIBUTING.md](CONTRIBUTING.md). Security reports: [SECURITY.md](SECURITY.md).
MIT — see [LICENSE](LICENSE).
