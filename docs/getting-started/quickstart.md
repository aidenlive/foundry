# Quickstart

Ten minutes from clone to a planned VPC, using the shipped `demo` project on
DigitalOcean.

## 1. See the configuration

```bash
foundry config projects            # → demo
foundry config environments        # → dev, staging, prod
foundry config render -p demo -e dev
```

The render is the *entire truth* for demo/dev: org metadata, provider,
region, network CIDR, Kubernetes sizing, labels, computed names.

Ask where any value comes from:

```bash
foundry config get -p demo -e prod kubernetes
# spec.kubernetes.minNodes: 3        (config/environments/prod.yaml)
# spec.kubernetes.nodeSize: s-2vcpu-4gb   (config/projects/demo.yaml)
```

## 2. Dry-run a stack

```bash
foundry stack plan -p demo -e dev -s network --dry-run
```

`--dry-run` prints exactly what would run and writes the generated inputs:

- `stacks/demo/network/.foundry/stack.tfvars.json` — full config context,
  exposed to HCL as `var.foundry_context`
- `stacks/demo/network/.foundry/backend.hcl` — remote state pointer derived
  from `spec.state`

## 3. Plan for real

```bash
export DIGITALOCEAN_TOKEN=…        # provider credentials
export AWS_ACCESS_KEY_ID=…         # Spaces keys for the state backend
export AWS_SECRET_ACCESS_KEY=…
foundry stack plan -p demo -e dev -s network
foundry stack apply -p demo -e dev -s network
```

Production is deliberately harder: `foundry stack apply -e prod` refuses
without `--allow-prod`.

## 4. Scaffold a service

```bash
foundry new service ./services/shop --var service_name=shop
cd services/shop && make run
curl localhost:8080/healthz
```

You get a hardened container, Kubernetes manifests with probes and limits,
CI that pushes to GHCR, and `/metrics` out of the box.

## Next

- [Concepts](concepts.md) for the mental model.
- [Configuration model](../configuration/model.md) to add your own org,
  projects, and environments.
