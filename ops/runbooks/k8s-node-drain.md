# Runbook: Kubernetes Node Maintenance / Drain

**Trigger:** node upgrades, resizing the pool, degraded node, or provider
maintenance notice.

Foundry clusters use surge upgrades + autoscaling pools, so *planned version
upgrades usually need nothing manual* — this runbook is for the exceptions.

## Preconditions

- `kubectl` context set to the right cluster
  (`doctl kubernetes cluster kubeconfig save <cluster_name>` — get the name
  from `foundry stack output -p <project> -e <env> -s platform`).
- Workloads have ≥2 replicas and PodDisruptionBudgets; single-replica
  workloads will take downtime — announce it.

## Drain a single node

```bash
kubectl get nodes -o wide                     # pick the victim
kubectl cordon <node>                         # stop new scheduling
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data --timeout=5m
```

If drain hangs: `kubectl get pdb -A` to find the blocking budget. Fix the
budget/replicas rather than forcing, unless this is an emergency
(`--force` evicts unmanaged pods and **loses their work**).

Then remediate the node (provider-side recycle for managed pools):

```bash
doctl kubernetes cluster node-pool list <cluster>
doctl kubernetes cluster node delete-node <cluster> <pool> <node-id>
```

The pool replaces it; `kubectl uncordon` is only needed if you kept the node.

## Resize the pool

Change `spec.kubernetes.minNodes/maxNodes` in
`config/environments/<env>.yaml`, then:

```bash
foundry stack apply -p <project> -e <env> -s platform [--allow-prod]
```

Never resize in the console — it will be reverted as drift.

## Verification

- `kubectl get nodes` all `Ready`, expected count.
- `kubectl get pods -A | grep -v Running` empty (or explained).
- App health endpoints green.

## Rollback

Nodes are cattle: if a replacement misbehaves, delete it and let the pool
recreate. For a bad version rollout, pin `spec.kubernetes.version` in config
to the previous version and apply.
