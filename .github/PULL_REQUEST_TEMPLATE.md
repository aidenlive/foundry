## What

<!-- One or two sentences: what changes and why. -->

## Checklist

- [ ] `make validate` passes locally (lint, tests, config, HCL, docs)
- [ ] Module contract unchanged, or the change is reflected in every provider
      implementation and the capability README
- [ ] Docs / runbooks updated where behavior changed
- [ ] No plaintext secrets; new secret material uses `foundry secrets`
- [ ] Production-affecting changes call out the rollout and rollback plan
