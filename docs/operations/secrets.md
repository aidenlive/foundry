# Secrets

## Model

- **Repo secrets** — application/infra values that belong with config:
  `config/secrets/<env>.enc.yaml`, encrypted with **sops + age**. Encrypted
  files are safe to commit; keys never are.
- **CI secrets** — provider and state credentials: GitHub *environment*
  secrets, scoped so dev workflows cannot see prod credentials.
- **Never**: plaintext in YAML, `foundry.local.yaml`, tfvars, or logs.
  `foundry validate` fails plaintext YAML under `config/secrets/`; gitleaks
  guards the rest of the tree in pre-commit.

## Daily use

```bash
foundry secrets edit config/secrets/dev.enc.yaml    # decrypt → $EDITOR → re-encrypt
foundry secrets view config/secrets/dev.enc.yaml    # read-only to stdout
foundry secrets encrypt path/to/new.yaml            # first-time encryption
```

Recipients (who can decrypt) are governed by `.sops.yaml` — replace the
placeholder age key with your own (`age-keygen`) before first use. Per-file
rules let prod secrets have a stricter recipient set than dev.

## Consuming secrets

Terraform: read the decrypted value at apply time and feed it as a variable
— e.g. `foundry secrets view … | yq .token` in the pipeline step, or the
sops provider if you prefer in-graph decryption. Kubernetes: create
`Secret` objects at deploy time from the same source; consider
external-secrets or sealed-secrets as the fleet grows.

The invariant either way: **decrypted material exists only in memory or in
the consumer**, never re-serialized into the repo.

## Rotation

Values quarterly, credentials on personnel change or exposure — full
procedures (including rotating the age recipients themselves) in
`ops/runbooks/secret-rotation.md`.
