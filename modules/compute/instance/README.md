# compute/instance

A single hardened virtual machine.

## Contract

| Variable          | Type           | Default | Notes                                       |
| ----------------- | -------------- | ------- | ------------------------------------------- |
| `name`            | `string`       | —       |                                             |
| `labels`          | `map(string)`  | `{}`    |                                             |
| `size`            | `string`       | —       | Provider-native size/machine type           |
| `image`           | `string`       | per-provider Ubuntu 22.04 LTS | Provider-native image ref |
| `subnet_id`       | `string`       | —       | Subnet (aws/gcp/azure) or VPC UUID (DO)     |
| `region`          | `string`       | —       | Region / location / zone as appropriate     |
| `ssh_public_key`  | `string`       | `""`    | Injected when set                           |
| `allow_ssh_cidrs` | `list(string)` | `[]`    | **SSH stays closed unless CIDRs provided**  |
| `user_data`       | `string`       | `""`    | cloud-init                                  |
| `public_ip`       | `bool`         | `false` | Attach a public address                     |

Outputs: `instance_id`, `private_ip`, `public_ip`.

## Security defaults

Root/OS disks encrypted at rest; instance metadata hardened (IMDSv2 on AWS);
no inbound traffic allowed until `allow_ssh_cidrs` (or stack-level rules) open
it; public IPs off by default.
