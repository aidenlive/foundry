# ADR-0002: Layered configuration is the single source of truth

**Status:** accepted · **Date:** 2026-07-01

## Context

Infrastructure values (regions, sizes, CIDRs, names, budgets) tend to
scatter: tfvars per stack, CI variables, wiki pages, heads. Duplication
drifts; nobody can answer "what is prod's CIDR" with confidence. We want one
authoritative, diffable, validatable place, with environment differences
expressed as *overrides* rather than copies.

## Decision

All configuration lives in versioned YAML documents
(Organization / Project / Environment, `apiVersion: foundry/v1`) merged with
explicit precedence — org < project < environment < local — where maps
deep-merge and scalars/lists replace. Every consumer (Terraform, templates,
env files, CI) receives *rendered* output from the `foundry` CLI; per-leaf
provenance is tracked so any value can be traced to its file. JSON Schemas
plus cross-document invariants gate every change.

## Consequences

- One diff answers "what changed about prod"; one command answers "why is
  this value X".
- Rendered artifacts (`.foundry/`, tfvars) become disposable build products
  — hand-editing them is drift by definition.
- The CLI is a hard dependency of the workflow; it must stay boring, fast,
  and dependency-light (Python stdlib + PyYAML + jsonschema).
- Schema evolution requires discipline (see CONTRIBUTING); the `apiVersion`
  field is the escape hatch for breaking changes.
