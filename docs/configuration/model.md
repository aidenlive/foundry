# The configuration model

All configuration lives under `config/` as Kubernetes-style documents:

```yaml
apiVersion: foundry/v1
kind: Organization | Project | Environment
metadata:
  name: …
spec:
  …
```

## Files

| File                              | Kind         | Scope                       |
| --------------------------------- | ------------ | --------------------------- |
| `config/foundry.yaml`             | Organization | Global defaults             |
| `config/projects/<p>.yaml`        | Project      | One deliverable             |
| `config/environments/<e>.yaml`    | Environment  | One blast-radius boundary   |
| `foundry.local.yaml` (gitignored) | any spec     | Personal experiments        |

## What the Organization spec covers

```yaml
spec:
  defaultProvider: digitalocean
  providers:                    # per-provider defaults
    digitalocean: {region: nyc3}
    aws: {region: us-east-1}
  naming: {delimiter: "-", pattern: "{org}-{project}-{environment}-{component}"}
  labels: {managed-by: foundry, …}
  network: {supernet: 10.0.0.0/8}
  security: {sshAllowedCidrs: [], enforceEncryption: true, imdsV2Required: true}
  state: {backend: s3, bucket: …, region: …, endpoint: …}   # DO Spaces works
  toolchain: {iac: {preferred: tofu, minVersion: "1.6.0"}, python: ">=3.10"}
  observability: {…}
  cost: {currency: USD, monthlyBudget: …}
```

Projects override sparsely — a demo project is ~15 lines: name, description,
stacks to deploy, Kubernetes sizing. Environments carry the CIDR, tier, and
tier-driven toggles (HA, deletion protection).

## The rendered context

`foundry config render -p <p> -e <e>` produces the structure every consumer
sees — exporters, templates, and stacks (as `var.foundry_context`):

```json
{
  "foundry": {"apiVersion": "foundry/v1"},
  "org":         {"name": "…", "domain": "…", "repository": "…"},
  "project":     {"name": "…", "description": "…"},
  "environment": {"name": "…", "tier": "…"},
  "spec":        { merged spec of all layers },
  "computed": {
    "provider": "digitalocean",
    "region": "nyc3",
    "tier": "production",
    "name_prefix": "standardcompute-demo-prod",
    "labels": { … },
    "state_key_prefix": "standardcompute/demo/prod"
  }
}
```

`spec` is the merge; `computed` is derived convenience. Consume `computed`
where possible — it encodes the conventions so stacks don't reimplement them.

## Exports

The same context renders to whatever a consumer needs:

```bash
foundry config export -p demo -e dev --format tfvars   > dev.tfvars.json
foundry config export -p demo -e dev --format dotenv   > .env.dev
foundry config export -p demo -e dev --format backend  > backend.hcl
foundry config export -p demo -e dev --format yaml|json
```

`foundry stack` runs the tfvars and backend exports automatically; the others
exist for services, scripts, and CI that want the same truth.
