# Concepts

Six words carry the whole vocabulary.

**Organization** — `config/foundry.yaml`. Global identity (name, domain,
repository) and defaults for everything: provider and regions, naming and
labels, network supernet, security posture, state backend, toolchain,
observability, cost guardrails.

**Project** — `config/projects/<name>.yaml`. A deliverable with its own
lifecycle: which stacks it deploys, project-specific sizing or overrides.

**Environment** — `config/environments/<name>.yaml`. A blast-radius boundary
(dev, staging, prod) with a **tier** (`nonproduction` or `production`).
Tier drives behavior: production enables deletion protection, HA, and the
`--allow-prod` guard.

**Context** — the deep merge of the three layers (plus optional
`foundry.local.yaml`) for one `(project, environment)` pair, enriched with
computed values: resolved provider and region, `name_prefix`, label map,
state key prefix. Stacks receive it verbatim as `var.foundry_context`.

**Module** — a reusable capability under `modules/`, one contract per
capability, one implementation per provider. Modules never read config;
stacks feed them values from the context.

**Stack** — a deployable Terraform/OpenTofu root under `stacks/` with its own
state file. Stacks compose modules and are driven entirely by the injected
context: `foundry stack plan|apply -p <project> -e <env> -s <stack>`.

One diagram of who talks to whom:

```
Organization ─┐
Project ──────┼─ merge ─▶ Context ─▶ Stack ─▶ Modules ─▶ Provider APIs
Environment ──┘              │
                             └────▶ templates, exports, names, labels
```

Change flows one way: edit config → validate → plan → apply. Anything edited
downstream (console clicks, hand-edited tfvars) is drift, and the nightly
drift workflow will file an issue about it.
