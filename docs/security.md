# Security

Defense in depth, with the boring parts automated.

## Identity and access

- **Humans**: least-privilege provider access per person; no shared logins.
  GitHub environment protection gates staging/prod applies behind review.
- **CI**: credentials are GitHub *environment* secrets — the dev pipeline
  physically lacks prod tokens. Rotate on the schedule in the
  secret-rotation runbook.
- **Workloads**: prefer platform identity (GKE Workload Identity, AKS
  managed identity, EKS IRSA) over long-lived keys; the cluster modules
  enable the prerequisites.

## Network posture

Deny by default. VPC modules open nothing inbound; instance modules keep SSH
closed until `allow_ssh_cidrs` is explicitly non-empty; "public" is an
explicit choice (`public_ip = true`, public subnets) visible in review.
Org-wide `spec.security.sshAllowedCidrs: []` means even that door needs a
config change to open.

## Data

Encryption at rest everywhere the modules touch: KMS-encrypted S3, encrypted
EBS/PD/managed disks, TLS-1.2-minimum storage accounts, private buckets with
versioning (which doubles as the state-file safety net — see the DR runbook).

## Secrets

sops + age, enforced: `foundry validate` fails on plaintext YAML under
`config/secrets/`, gitleaks runs in pre-commit, and the
[secrets guide](operations/secrets.md) covers rotation and recipient
management. CI secrets live in GitHub environments, never in the repo.

## Change safety

- `--allow-prod` required for production apply/destroy — a speed bump
  exactly where speed hurts.
- `tier: production` flips deletion protection and HA defaults in config.
- Nightly drift detection turns console cowboying into filed issues.
- Module security defaults are contractual: PRs weakening them are treated
  as vulnerabilities (see SECURITY.md at the repo root for reporting).

## What Foundry does *not* do

No WAF/CDN opinions, no runtime IDS, no policy engine (OPA/Sentinel) — yet.
The config model gives those tools a single place to plug in when you adopt
them.
