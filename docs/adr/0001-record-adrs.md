# ADR-0001: Record architecture decisions

**Status:** accepted · **Date:** 2026-07-01

## Context

Foundry encodes many opinionated choices (config precedence, provider
abstraction strategy, tooling). The *why* evaporates unless written down at
decision time; new contributors and future maintainers re-litigate settled
questions without it.

## Decision

Record significant architecture decisions as short ADRs in `docs/adr/`,
numbered sequentially, in Michael Nygard's format (Context / Decision /
Consequences). "Significant" = expensive to reverse, or shapes how
contributors work. ADRs are immutable once accepted; changing course means a
new ADR that supersedes the old one.

## Consequences

- The reasoning survives contributor turnover; reviews can point at ADRs
  instead of repeating arguments.
- Slight friction on big changes — intended.
- The nav in `mkdocs.yml` gains one line per decision.
