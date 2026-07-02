# {{ foundry.service_name }}

{{ foundry.description }}

Scaffolded by [Foundry](https://github.com/standardcompute/foundry) for
{{ foundry.org }} — {{ foundry.year }}.

## Run

```
make run                 # local, no dependencies beyond Python 3.10+
make docker-run          # containerized
curl localhost:{{ foundry.port }}/healthz
```

## Endpoints

| Path       | Purpose                              |
| ---------- | ------------------------------------ |
| `/`        | Service banner (JSON)                |
| `/healthz` | Liveness — process is up             |
| `/readyz`  | Readiness — safe to receive traffic  |
| `/metrics` | Prometheus text exposition           |

## Deploy

`deploy/k8s/` holds environment-agnostic manifests; set the image and apply:

```
kubectl apply -f deploy/k8s/
```

CI (`.github/workflows/ci.yml`) builds and pushes
`ghcr.io/<owner>/{{ foundry.service_name }}` on every push to `main`.
