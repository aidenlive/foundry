# Foundry

Foundry is Standard Compute Org's open-source toolkit for running
infrastructure the same way everywhere: **configuration is the single source
of truth**, and everything else — Terraform inputs, state backends, resource
names, labels, env files, scaffolds — is rendered from it.

## The shape of it

```
config/*.yaml ──▶ foundry CLI ──▶ stacks (OpenTofu/Terraform) ──▶ cloud
     ▲                │
     │                └──▶ templates, env files, docs, machine context
     └── org < project < environment < local overrides
```

Three ideas carry the whole system:

**Layered configuration.** An `Organization` document sets defaults; `Project`
and `Environment` documents override only what differs. Every rendered value
knows which file it came from (`foundry config get … ` shows you).

**Contracts over providers.** Each capability — `network/vpc`,
`compute/instance`, `kubernetes/cluster`, `storage/object-store`, `dns/zone` —
defines one variable/output contract with four interchangeable
implementations (AWS, GCP, Azure, DigitalOcean). Migrating clouds is a config
change plus one `source` line per module.

**Guardrails by default.** Encryption at rest, deny-by-default ingress, IMDSv2,
private buckets, sops-encrypted secrets, `--allow-prod` on destructive
production actions, CI environment protection, nightly drift detection.

## Where to go

- New here → [Installation](getting-started/installation.md) then the
  [Quickstart](getting-started/quickstart.md).
- Wiring your own org → [The configuration model](configuration/model.md).
- Writing infrastructure → [Modules](modules/overview.md) and
  [Stacks](stacks.md).
- Running it in anger → [CI/CD](ci-cd.md), [Security](security.md), and the
  runbooks in `ops/`.
- An AI agent → `AGENTS.md` at the repo root, `docs/llms.txt`, or
  `foundry context --format json`.
