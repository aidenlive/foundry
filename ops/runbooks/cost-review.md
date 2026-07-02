# Runbook: Monthly Cost Review

**Trigger:** first business day of the month, or a billing alert.

Foundry's leverage on cost is that **every resource carries labels**
(`managed-by`, `org`, `project`, `environment`), so spend can always be
grouped by owner.

## 1. Pull the numbers (15 min)

- Provider billing consoles, grouped by tag/label `project` then
  `environment`. On DigitalOcean group by tag; on AWS use Cost Explorer
  filtered to `managed-by=foundry`.
- Note month-over-month deltas > 10 % and any resource with no `project`
  label — unlabeled spend is a bug; find and import or delete it.

## 2. Hunt the usual suspects (30 min)

- **Dev running hot:** dev/staging exceeding
  `spec.cost.monthlyBudget` — check `maxNodes`, forgotten load-test
  clusters, oversized droplets.
- **Orphans:** unattached volumes/IPs, empty clusters, LBs pointing at
  nothing. Compare live resources against `foundry stack output` per stack;
  anything live-but-not-in-state is either manual (import or delete) or
  leaked.
- **Storage growth:** bucket versioning without lifecycle rules grows
  forever; confirm retention still matches intent.
- **NAT and egress:** on AWS, NAT gateway hours + data processing are the
  classic silent line item.

## 3. Act through config, not consoles

Right-size by editing config (`spec.kubernetes.nodeSize`, `maxNodes`,
instance sizes) and applying the affected stacks. Record accepted increases
by raising `spec.cost.monthlyBudget` in the same PR that explains why.

## 4. Report

One short note in `#ops`: total by environment, delta vs last month, actions
taken, actions deferred (with owners). Link the PRs. File `ops`-labeled
issues for anything not fixed this cycle.
