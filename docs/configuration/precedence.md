# Precedence and provenance

## The rule

Later layers win, per value:

```
Organization  <  Project  <  Environment  <  foundry.local.yaml
```

- **Maps deep-merge.** Setting `spec.kubernetes.minNodes` in prod doesn't
  erase `nodeSize` from the project layer.
- **Scalars and lists replace.** A list is a decision, not a suggestion —
  `sshAllowedCidrs: []` in prod means *empty*, regardless of what dev allows.

## Why lists replace

Merging lists has no universally right semantics (append? union? position?),
and security-relevant lists must never silently inherit. Replacement keeps
every list's final value visible in exactly one file.

## Provenance

Every leaf remembers its origin file. Two ways to see it:

```bash
foundry config get -p demo -e prod kubernetes.minNodes
# 3    (config/environments/prod.yaml)

foundry config render -p demo -e prod --origins
# annotates every value with its source layer
```

When a value surprises you, ask `config get` before grepping — the answer
includes the file that won.

## Local overrides

`foundry.local.yaml` at the repo root (gitignored) merges last. Use it to
point dev at a personal region or shrink node counts while experimenting.
It is a footgun in CI by design: CI checkouts never have one, so CI always
renders the committed truth.

!!! warning
    Never put secrets in `foundry.local.yaml` — it's plaintext. Secrets go
    through [sops](../operations/secrets.md).
