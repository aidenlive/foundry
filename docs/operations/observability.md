# Observability

Foundry standardizes the *contract* so any backend can consume it; it does
not ship a monitoring stack.

## The service contract

Every service scaffolded by `foundry new service` exposes:

| Endpoint   | Meaning                                        |
| ---------- | ---------------------------------------------- |
| `/healthz` | liveness — the process is up                   |
| `/readyz`  | readiness — safe to receive traffic (drains on SIGTERM) |
| `/metrics` | Prometheus text format                         |

plus **JSON logs to stdout** (`ts`, `level`, `service`, `msg`, fields).
Kubernetes manifests wire the probes; any Prometheus-compatible agent
(DO managed monitoring, Grafana Agent, Datadog) can scrape `/metrics`
unmodified.

## Infrastructure signals

- **Labels are the join key.** Every module applies
  `managed-by/org/project/environment`, so provider metrics and cost
  dashboards can group by the same dimensions as your config.
- Enable provider-native basics per environment via config
  (`spec.observability`): DO monitoring is on for droplets; cluster modules
  leave room for log/metric agents as a follow-on stack.
- **Drift is a signal**: the nightly workflow's issues are your
  infrastructure alerting channel of last resort.

## Alerting baseline

Start with three alerts per production service and grow from need:

1. availability (health check fails from outside),
2. saturation (node/pool at max for > 15 min),
3. budget (provider billing alert at 80 % of `spec.cost.monthlyBudget`).

Route to a human with a pager; dashboards link from each service README.

## SLOs

When ready, define per-service SLOs on the `/metrics` request counters
(latency histograms are the natural next addition to the template). Keep the
targets in the service README next to the dashboard link — where the
on-call will actually look.
