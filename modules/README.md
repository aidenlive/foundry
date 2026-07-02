# Foundry Modules

Cloud-agnostic infrastructure building blocks. Every **capability** (network,
compute, kubernetes, storage, dns) defines one input/output **contract**; each
supported provider implements that contract in its own subdirectory.

```
modules/<capability>/<component>/<provider>/
```

Because Terraform/OpenTofu module sources must be static strings, stacks pick
the implementation by path — usually derived from Foundry config:

```hcl
module "vpc" {
  # provider chosen in config/…yaml → computed.provider
  source = "../../../modules/network/vpc/digitalocean"

  name   = module.labels.name_prefix
  labels = module.labels.labels
  cidr   = var.foundry_context.spec.network.cidr
}
```

## Capability matrix

| Capability            | aws | gcp | azure | digitalocean |
| --------------------- | :-: | :-: | :---: | :----------: |
| foundation/labels     |  ✓ (provider-free)              ||||
| network/vpc           |  ✓  |  ✓  |   ✓   |      ✓       |
| compute/instance      |  ✓  |  ✓  |   ✓   |      ✓       |
| kubernetes/cluster    |  ✓  |  ✓  |   ✓   |      ✓       |
| storage/object-store  |  ✓  |  ✓  |   ✓   |      ✓       |
| dns/zone              |  ✓  |  ✓  |   ✓   |      ✓       |

## Rules

1. **Contract first.** Same variable and output names across providers; add
   provider-specific knobs only with safe defaults.
2. **Secure by default.** Encryption at rest on, public ingress denied, SSH
   closed unless CIDRs are passed, IMDSv2 required, no plaintext secrets.
3. **Labels always.** Every implementation accepts `labels` and applies them
   (tags on AWS/Azure/DO, labels on GCP) so cost and ownership reporting work.
4. **Small and boring.** Prefer plain resources over clever meta-programming;
   modules must parse with `scripts/check_hcl.py` and read in one sitting.
