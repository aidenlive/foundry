# Checklist: Production Readiness

Gate before an environment is declared `tier: production` or a new service
takes production traffic. PR the completed checklist into the service/project
docs.

## Configuration

- [ ] Environment document exists, `foundry validate` green, CIDRs
      non-overlapping with every other environment
- [ ] `tier: production` set — deletion protection and HA defaults engage
- [ ] Budgets set (`spec.cost.monthlyBudget`) and alerting recipients real

## Infrastructure

- [ ] State backend: versioned bucket, credentials scoped to CI + operators
- [ ] `foundry stack plan` clean on every stack (no drift at launch)
- [ ] HA where it matters: prod K8s control plane HA, `minNodes ≥ 2`,
      multi-AZ subnets on providers that have them
- [ ] No public ingress except intended edges; SSH closed
      (`allow_ssh_cidrs` empty) or bastion-only

## Operations

- [ ] Monitoring: health endpoints scraped, alerts routed to a human with
      a pager, dashboards linked from the service README
- [ ] Runbooks read by ≥2 people; incident-response roles assigned
- [ ] DR: state-restore rehearsed once (Runbook: dr-restore, section A)
- [ ] Secrets in sops only; rotation owner named; `gitleaks` in pre-commit

## Delivery

- [ ] CI: plan on PR, apply via protected environment with required reviewer
- [ ] Drift workflow covers all prod stacks (matrix updated)
- [ ] Rollback path documented for both workloads and infra

Sign-off: ______________  Date: __________
