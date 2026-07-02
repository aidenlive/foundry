# ADR-0003: Cloud-agnostic capability contracts, per-provider implementations

**Status:** accepted · **Date:** 2026-07-01

## Context

We start on DigitalOcean for cost and simplicity but must credibly reach
AWS/GCP/Azure without a rewrite. Alternatives considered: (a) one module with
`count`-guarded resources for every provider — unreadable, untestable;
(b) provider-specific modules with divergent interfaces — every stack
rewrite is a migration; (c) a translation layer/DSL above Terraform — heavy,
leaky.

## Decision

Each capability (`network/vpc`, `compute/instance`, `kubernetes/cluster`,
`storage/object-store`, `dns/zone`) defines **one variable/output contract**
in its README; each provider gets its own conforming implementation
directory. Stacks select implementations by source path (config-driven
convention). Provider gaps are documented and papered over with type-stable
outputs; provider extras are opt-in with safe defaults. Security defaults
are part of the contract.

## Consequences

- Switching providers touches config plus one `source` line per module —
  wiring and variables survive.
- 4× implementation cost per capability; accepted, and bounded by keeping
  modules small ("boring") and the capability set curated.
- The contract README is load-bearing documentation; CI parses all
  implementations and CODEOWNERS gates changes.
- Lowest-common-denominator risk is managed by allowing documented
  provider-specific inputs rather than forbidding them.
