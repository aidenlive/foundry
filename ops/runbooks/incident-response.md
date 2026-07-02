# Runbook: Incident Response

**Trigger:** production impact — outage, severe degradation, data integrity
concern, or security event.

## Roles

Smallest useful set. One person may hold several early on:

- **Incident Commander (IC)** — owns coordination and decisions; does not debug.
- **Operator** — hands on keyboard.
- **Comms** — posts status updates (status page, stakeholders) every 30 min.

## 1. Declare and stabilize (first 10 minutes)

1. Declare in `#incidents`: what is broken, who is IC, severity
   (S1 total outage / S2 degraded / S3 minor).
2. Open a shared doc; log every action **with timestamps** as you go.
3. Check the obvious inputs first:

   ```bash
   kubectl get nodes && kubectl get pods -A | grep -v Running
   kubectl get events -A --sort-by=.lastTimestamp | tail -20
   foundry stack output -p <project> -e prod -s platform
   ```

4. Correlate with change history: last merged PR, last apply
   (Actions → terraform), last drift issue.

## 2. Mitigate first, diagnose second

Prefer the fastest safe path back to service:

- **Bad deploy** → roll back the workload
  (`kubectl rollout undo deployment/<name>`).
- **Bad infra change** → revert the config/stack PR, then
  `foundry stack apply -p <project> -e prod -s <stack> --allow-prod`.
- **Capacity** → raise `maxNodes` in `config/environments/prod.yaml`, apply
  the platform stack; autoscaling handles the rest.
- **Suspected compromise** → do NOT destroy evidence; isolate (cordon nodes,
  revoke credentials via the secret-rotation runbook) and involve the
  security owner immediately.

Never hand-edit cloud resources in the console except to stop active harm —
note anything you touched so it can be reconciled in code afterwards.

## 3. Verify

Health endpoints green, error rates back to baseline, a fresh
`foundry stack plan` on the affected stack shows no unexpected diff.

## 4. Close out

1. Comms posts resolution; IC closes the incident thread.
2. Within 48 h: blameless postmortem — timeline, impact, root cause,
   contributing factors, action items with owners.
3. File action items as issues labeled `ops`; update this runbook if it was
   wrong or incomplete.
