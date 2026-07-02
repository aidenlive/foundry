# Operations

Procedures for running Foundry-managed infrastructure.

- `runbooks/` — step-by-step responses to specific situations (incidents,
  restores, rotations, upgrades, cost reviews). Written to be followed
  verbatim at 3 a.m. by someone who did not write them.
- `checklists/` — gates for recurring milestones (production readiness,
  onboarding).

Conventions: every runbook states its trigger, preconditions, steps,
verification, and rollback. Commands are copy-pasteable and assume an
activated Foundry environment (`source .venv/bin/activate`). When a runbook
and reality disagree, fix the runbook in the same PR that fixes reality.
