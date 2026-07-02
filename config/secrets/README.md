# Secrets

Foundry never stores plaintext secrets in git. Encrypted secrets live in this
directory as SOPS-encrypted YAML (`*.enc.yaml`), governed by the repository
root `.sops.yaml`.

Workflow:

1. `foundry secrets init` — verifies `sops` + `age` are installed and prints
   key-generation instructions.
2. Add your age public key to `.sops.yaml` at the repository root.
3. `foundry secrets edit config/secrets/dev.enc.yaml` — create/edit through
   sops so plaintext never touches disk unencrypted.
4. In CI, decrypt with a key held in your CI secret store (or use cloud KMS
   via sops); at runtime prefer a secret manager / External Secrets Operator.

Plaintext YAML files in this directory are rejected by the pre-commit
`gitleaks` hook and by `foundry validate`.
