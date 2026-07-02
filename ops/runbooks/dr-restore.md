# Runbook: Disaster Recovery — State and Environment Restore

**Trigger:** Terraform state lost/corrupted, or an environment must be
rebuilt (region failure, catastrophic deletion).

**Preconditions:** state bucket versioning is ON (Foundry's object-store
module default), provider credentials available, this repo at the commit
matching production.

## A. Restore a corrupted/lost state file

State lives at
`s3://<spec.state.bucket>/<org>/<project>/<environment>/<stack>.tfstate`.

1. Freeze writes: announce in `#ops`; pause the drift and deploy workflows.
2. List versions and identify the last good one:

   ```bash
   aws s3api list-object-versions \
     --endpoint-url https://<region>.digitaloceanspaces.com \
     --bucket <state-bucket> \
     --prefix standardcompute/demo/prod/network.tfstate
   ```

3. Copy the good version back into place (same command family with
   `--version-id`), keeping a local backup of the bad one first.
4. Verify integrity:

   ```bash
   foundry stack plan -p demo -e prod -s network
   ```

   Expect **no changes**. A wall of creates means the state is older than
   reality — stop and reconcile with `tofu state ls` / targeted imports
   before proceeding.

## B. Rebuild an environment from scratch

Order matters; stacks are applied in dependency order.

1. Confirm config is the truth: `foundry validate` and
   `foundry config render -p <project> -e <env>` review.
2. Apply foundational stacks first:

   ```bash
   foundry stack apply -p demo -e prod -s network --allow-prod
   foundry stack apply -p demo -e prod -s platform --allow-prod -- -var vpc_id=<from network output>
   ```

3. Restore data (managed database snapshots, bucket sync from backup) —
   data restore procedures live with each service's own runbook.
4. Redeploy workloads (CI re-run or `kubectl apply` of service manifests).
5. Repoint DNS last, after health checks pass.

## Verification

- `foundry stack plan` clean on every stack.
- Application health endpoints green; smoke tests pass.
- New state file versions present in the bucket.

## Afterwards

Postmortem (see incident-response). If versioning saved you, say so in the
postmortem — it is the cheapest insurance we buy.
