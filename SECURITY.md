# Security Policy

## Supported versions

The latest minor release receives security fixes.

## Reporting a vulnerability

Email **security@standardcompute.org** or use GitHub private vulnerability
reporting. Please do **not** open public issues for suspected
vulnerabilities.

Include reproduction steps, affected component (CLI, module, workflow), and
impact. You will receive an acknowledgment within 72 hours and a remediation
plan or fix timeline within 14 days. We credit reporters in release notes
unless you prefer otherwise.

## Scope notes

- Secrets belong in `config/secrets/*.enc.yaml` (sops + age) — a plaintext
  secret in the repo is always a valid report.
- Module security defaults (encryption at rest, deny-by-default ingress,
  IMDSv2, private buckets) are contractual; regressions are treated as
  vulnerabilities, not style issues.
