# Modules overview

`modules/` holds the reusable building blocks:

```
modules/<capability>/<component>/<provider>/
modules/foundation/labels/            # provider-free
```

| Capability             | Component     | aws | gcp | azure | digitalocean |
| ---------------------- | ------------- | :-: | :-: | :---: | :----------: |
| foundation             | labels        | ✓ (provider-free) ||||
| network                | vpc           |  ✓  |  ✓  |   ✓   |      ✓       |
| compute                | instance      |  ✓  |  ✓  |   ✓   |      ✓       |
| kubernetes             | cluster       |  ✓  |  ✓  |   ✓   |      ✓       |
| storage                | object-store  |  ✓  |  ✓  |   ✓   |      ✓       |
| dns                    | zone          |  ✓  |  ✓  |   ✓   |      ✓       |

Each capability directory has a README that *is* the contract: variables,
outputs, defaults, and per-provider notes (including honest documentation of
provider gaps — e.g. DigitalOcean VPCs have no subnets, so subnet outputs are
empty lists there).

## Selecting an implementation

Module sources are static strings in Terraform, so provider selection is a
path convention driven by config:

```hcl
module "vpc" {
  # computed.provider for this project/environment
  source = "../../../modules/network/vpc/digitalocean"
  …
}
```

Changing clouds for an environment = change `spec.defaultProvider` (or the
project override), update the `source` lines in its stacks, plan, migrate.
The variables you pass do not change — that's the point of the contract.

## Security defaults

Baked into every implementation, not optional inputs:

- storage: private ACLs / public-access blocks, encryption at rest, versioning
- compute: encrypted root disks, IMDSv2 (AWS), shielded VM (GCP), SSH closed
  until `allow_ssh_cidrs` is explicitly non-empty
- network: no open ingress; NAT is opt-in and cost-visible
- kubernetes: autoscaling pools, auto-repair/upgrade, workload identity (GKE)

Weakening any of these belongs at the stack layer where it is visible in
review — never in the module.
