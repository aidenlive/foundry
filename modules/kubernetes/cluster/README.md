# kubernetes/cluster

A managed Kubernetes control plane with one autoscaling system node pool.

## Contract

| Variable      | Type          | Default    | Notes                                        |
| ------------- | ------------- | ---------- | -------------------------------------------- |
| `name`        | `string`      | —          |                                              |
| `labels`      | `map(string)` | `{}`       |                                              |
| `region`      | `string`      | —          |                                              |
| `version`     | `string`      | `""`       | Empty = provider-recommended / latest stable |
| `node_size`   | `string`      | —          | Provider-native size slug                    |
| `min_nodes`   | `number`      | `1`        |                                              |
| `max_nodes`   | `number`      | `3`        |                                              |
| `vpc_id`      | `string`      | —          | Network / VPC (UUID on DO)                   |
| `subnet_ids`  | `list(string)`| `[]`       | Required on aws/azure; unused on DO          |

Outputs: `cluster_id`, `cluster_name`, `endpoint`, `ca_certificate`
(sensitive), `version`.

Kubeconfig retrieval stays out of state where possible — prefer
`aws eks update-kubeconfig`, `gcloud container clusters get-credentials`,
`az aks get-credentials`, or `doctl kubernetes cluster kubeconfig save`.

## Provider notes

- **aws (EKS)** — creates the cluster + node IAM roles with AWS-managed
  policies, private+public endpoint, one managed node group.
- **gcp (GKE)** — removes the default pool, enables Workload Identity, uses a
  release channel when `version` is empty.
- **azure (AKS)** — SystemAssigned identity, one autoscaling default pool.
  Extra input: `resource_group_name`.
- **digitalocean (DOKS)** — node pool with auto-scale + surge upgrades;
  `version` empty resolves the latest patch of the default minor via the
  provider `digitalocean_kubernetes_versions` data source.
