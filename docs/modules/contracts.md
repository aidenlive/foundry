# Module contracts

A **contract** is the promise that lets stacks treat providers as
interchangeable: same variable names, same output names, same semantics.

## The rules

1. **One contract per capability.** Defined in the capability README
   (`modules/<capability>/<component>/README.md`); implementations conform.
2. **Same names everywhere.** `name`, `labels`, `region` are universal;
   capability-specific inputs (`cidr`, `node_size`, `versioning`, …) match
   across providers exactly.
3. **Provider extras are opt-in.** A provider may need more (Azure's
   `resource_group_name`, GCP's `project_id`) or offer more (DOKS
   `ha_control_plane`) — always with safe defaults or documented as
   provider-required, never silently changing shared semantics.
4. **Honest gaps.** Where a provider lacks a concept, accept the input for
   parity, document that it is ignored, and keep outputs type-stable (DO
   returns `[]` for subnet IDs rather than omitting the output).
5. **Outputs are the API.** Downstream stacks may rely on any documented
   output; removing or renaming one is a breaking change to every provider
   at once.

## Contract summary

| Capability            | Key inputs                                            | Outputs                                            |
| --------------------- | ----------------------------------------------------- | -------------------------------------------------- |
| network/vpc           | name, labels, cidr, region, public/private_subnets, enable_nat | vpc_id, public_subnet_ids, private_subnet_ids |
| compute/instance      | name, labels, size, image, subnet_id, ssh_public_key, allow_ssh_cidrs, user_data, public_ip | instance_id, private_ip, public_ip |
| kubernetes/cluster    | name, labels, region, version, node_size, min/max_nodes, vpc_id, subnet_ids | cluster_id, cluster_name, endpoint, ca_certificate, version |
| storage/object-store  | name, labels, region, versioning, force_destroy       | bucket_id, bucket_name                             |
| dns/zone              | name, labels                                          | zone_id, name_servers                              |

## Changing a contract

Treat it like a public API change:

1. Update the capability README first — it is the spec.
2. Update **all four** implementations in the same PR.
3. Add/adjust defaults so existing stacks keep planning clean.
4. Note the change in CHANGELOG.md; breaking changes bump the minor
   pre-1.0 (SemVer).

CI's HCL gate parses every implementation; CODEOWNERS routes `modules/`
changes to the platform team.
