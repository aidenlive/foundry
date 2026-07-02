# network/vpc

One private network per environment.

## Contract

| Variable          | Type           | Default | Notes                                   |
| ----------------- | -------------- | ------- | --------------------------------------- |
| `name`            | `string`       | —       | Usually `module.labels.name_prefix`     |
| `labels`          | `map(string)`  | `{}`    | Applied as tags/labels                  |
| `cidr`            | `string`       | —       | Environment CIDR from config            |
| `region`          | `string`       | —       | Provider region/location                |
| `public_subnets`  | `list(string)` | `[]`    | CIDRs (ignored on DO — see below)       |
| `private_subnets` | `list(string)` | `[]`    | CIDRs                                   |
| `enable_nat`      | `bool`         | `false` | Managed NAT for private egress          |

Outputs: `vpc_id`, `public_subnet_ids`, `private_subnet_ids`.

## Provider notes

- **aws** — VPC + IGW; public subnets map public IPs on launch; optional
  single NAT gateway (cost-conscious default) for private subnets.
- **gcp** — VPC network with custom-mode subnetworks. GCP has no
  public/private subnet split; "public" here means instances may attach
  external IPs, "private" subnetworks get Private Google Access. `enable_nat`
  creates Cloud Router + Cloud NAT.
- **azure** — Resource group (optionally pre-existing), VNet, subnets, and a
  default-deny NSG on private subnets. Extra output: `resource_group_name`.
- **digitalocean** — DO VPCs carry a single `ip_range` and no subnets; subnet
  inputs are accepted for contract compatibility and ignored, subnet outputs
  are empty lists. NAT is implicit.
