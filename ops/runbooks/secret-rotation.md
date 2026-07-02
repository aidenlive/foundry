# Runbook: Secret Rotation

**Trigger:** scheduled rotation (quarterly), personnel change, or suspected
exposure. For suspected exposure treat as an incident **and** rotate.

Secrets live in two places, rotated independently:

1. **Repo secrets** — `config/secrets/<env>.enc.yaml`, encrypted with
   sops + age (`.sops.yaml` holds recipients).
2. **CI secrets** — GitHub environment secrets (provider tokens, state
   credentials).

## Rotate a repo secret value

```bash
foundry secrets edit config/secrets/prod.enc.yaml   # opens decrypted in $EDITOR
# change the value, save, exit — file is re-encrypted on close
foundry validate                                     # confirms nothing plaintext
git commit -am "rotate <name> in prod secrets"
```

Then re-apply whatever consumes it (stack or service deploy).

## Rotate the age key itself (recipient change)

1. New keeper runs `age-keygen`; add the public key to `.sops.yaml`.
2. Re-encrypt every file to the new recipient set:

   ```bash
   for f in config/secrets/*.enc.yaml; do sops updatekeys -y "$f"; done
   ```

3. Remove departed recipients from `.sops.yaml`, run `updatekeys` again.
4. Commit both changes together; departed keys can no longer decrypt HEAD.
   (History remains decryptable to old keys — rotate the *values* too when
   someone leaves.)

## Rotate a provider/CI credential

1. Create the new credential in the provider console (DO API token, Spaces
   keypair, AWS access key…). Grant least privilege — clone the old one's
   scope, don't expand it.
2. Update the GitHub environment secret (repo → Settings → Environments).
3. Trigger a no-op run to prove the new credential works:

   ```bash
   gh workflow run drift.yml
   ```

4. Revoke the old credential only after a green run.
5. Log the rotation (date, credential, who) in the ops journal.

## Verification

- `foundry validate` green (secrets hygiene check).
- `gitleaks detect` clean.
- CI pipelines green with new credentials; old ones revoked.
