# Cost

Cost control in Foundry is a consequence of structure, not a dashboard.

## Structure that saves money

- **Labels on everything** (`project`, `environment`) — provider billing can
  always answer "who is spending". Unlabeled spend is treated as a bug.
- **Sizing lives in config** — `spec.kubernetes.nodeSize`, `min/maxNodes`,
  instance sizes are diffable, reviewable, and per-environment. Dev defaults
  small; prod capacity is an explicit, reviewed change.
- **Expensive things are opt-in**: NAT gateways (`enable_nat`), HA control
  planes (tier-driven), public IPs. Nothing costly appears by accident.
- **Budgets in config**: `spec.cost.monthlyBudget` per environment is the
  reference for billing alerts (set at ~80 %) and the monthly review.

## The rhythm

The monthly cost review (`ops/runbooks/cost-review.md`) is the whole
process: pull spend grouped by
label, hunt orphans and unlabeled resources, right-size through config PRs,
record accepted growth by raising the budget in the same PR that explains it.

## Cheap-by-default choices already made

- DigitalOcean as the starting provider (predictable flat pricing).
- Single NAT (not per-AZ) in the AWS VPC module default.
- Autoscaling node pools with low `minNodes` outside production.
- `gp3`/`pd-balanced`/Standard-LRS storage tiers as defaults.

Scaling up is a config change; scaling *spend* down later is archaeology.
Default small.
