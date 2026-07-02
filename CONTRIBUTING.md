# Contributing to Foundry

Thanks for helping make infrastructure boring. Small, focused pull requests
merge fastest.

## Development setup

```bash
./scripts/bootstrap.sh
source .venv/bin/activate
make validate        # lint + tests + config + HCL + docs — must pass
```

## Ground rules

1. **Config model changes** update the JSON Schemas, `foundry validate`
   checks, docs, and tests together — they are one unit.
2. **Module changes keep the contract.** If a variable or output changes,
   change it in *every* provider implementation and the capability README.
   Provider-specific knobs need safe defaults.
3. **Security defaults only tighten.** Anything that opens ingress, disables
   encryption, or weakens IMDS/identity settings must be opt-in and reviewed.
4. **Every behavior is testable.** CLI changes come with pytest coverage;
   HCL must pass `scripts/check_hcl.py`; docs build with `--strict`.
5. **Runbooks are code.** If your change alters an operational procedure,
   update `ops/`.

## Pull request flow

- Branch from `main`; use clear commit messages (imperative mood).
- Fill in the PR template checklist honestly.
- CI must be green; CODEOWNERS review is required on `modules/`, `config/`,
  and `.github/`.

## Releases

Maintainers tag `vX.Y.Z` (SemVer, matching `VERSION` and `CHANGELOG.md`);
the release workflow builds the CLI and publishes GitHub release artifacts.
