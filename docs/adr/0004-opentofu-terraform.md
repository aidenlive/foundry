# ADR-0004: Target OpenTofu first, remain Terraform-compatible

**Status:** accepted · **Date:** 2026-07-01

## Context

Terraform's license change (BUSL) makes long-term open-source alignment
uncertain; OpenTofu is the community fork under the Linux Foundation with a
compatible language and providers. Our modules use no features exclusive to
either. Contributors and CI environments may have either binary.

## Decision

Foundry is engine-agnostic at the HCL level and **prefers `tofu`** at run
time: `foundry stack` uses `spec.toolchain.iac.preferred`, falling back to
whichever of `tofu`/`terraform` is on PATH. CI pins OpenTofu
(`opentofu/setup-opentofu`). Modules declare `required_version >= 1.6.0` and
standard provider sources; we avoid engine-exclusive features until a
concrete need forces a revisit (which would be a new ADR).

## Consequences

- MIT-licensed toolkit rests on an open-source engine by default, while
  Terraform users lose nothing today.
- A registry-free syntax gate (`scripts/check_hcl.py`) keeps CI fast and
  offline-friendly; full `validate`/`plan` runs in the stack pipeline where
  credentials and providers exist.
- If the dialects diverge on a feature we need, we choose then — with usage
  data — rather than pre-committing now.
