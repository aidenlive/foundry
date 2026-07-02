# Schemas and validation

Every document kind has a JSON Schema (draft 2020-12) under `config/schema/`:

```
common.schema.json         shared definitions (names, CIDRs, labels)
organization.schema.json   kind: Organization
project.schema.json        kind: Project
environment.schema.json    kind: Environment
```

## What `foundry validate` checks

1. **Shape** — each document against its schema: required fields, enums
   (tiers, providers, backends), formats (DNS-safe names, CIDR syntax).
2. **Cross-document invariants** the schemas can't express:
   - environment CIDRs must not overlap each other and must sit inside
     `spec.network.supernet`;
   - every stack a project lists must resolve to a directory under `stacks/`;
   - naming pattern placeholders must be known variables;
   - **secrets hygiene** — YAML under `config/secrets/` that isn't
     sops-encrypted fails the build.

Run it locally after any config edit; CI runs it on every push:

```bash
foundry validate
# config/foundry.yaml                organization  OK
# config/projects/demo.yaml          project       OK
# config/environments/prod.yaml      environment   OK
# cross-checks: cidr-overlap OK, stacks OK, naming OK, secrets OK
```

## Evolving the schema

Schema, validator checks, docs, and tests move together (see
CONTRIBUTING.md). Additive fields with defaults are minor; breaking shape
changes bump `apiVersion` — documents declare `foundry/v1`, so a future
`foundry/v2` can coexist during migration.

Editors that support JSON Schema can bind
`config/schema/*.schema.json` to the YAML files for inline completion; the
schemas are plain files with no build step.
