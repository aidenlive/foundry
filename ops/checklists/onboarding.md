# Checklist: Engineer Onboarding

Target: productive, safe access on day one; first merged PR within a week.

## Access (owner: team lead)

- [ ] GitHub org membership + `@standardcompute/platform` team (if platform)
- [ ] Provider console access — least privilege, no shared accounts
- [ ] Added as age recipient for the secrets they genuinely need
      (Runbook: secret-rotation, recipient change)
- [ ] `#ops` and `#incidents` channels

## Local setup (owner: new engineer)

- [ ] Clone, `./scripts/bootstrap.sh`, `source .venv/bin/activate`
- [ ] `foundry doctor` — all required tools green (install what it flags)
- [ ] `make validate` passes locally
- [ ] `pre-commit install`
- [ ] Read: README, AGENTS.md, `stacks/README.md`, incident-response runbook

## First-week exercises

- [ ] Render dev config and explain one value's provenance
      (`foundry config get -p demo -e dev network.cidr`)
- [ ] `foundry stack plan -p demo -e dev -s network --dry-run` and walk
      through what the CLI generated in `.foundry/`
- [ ] Scaffold a service (`foundry new service …`), run it, hit `/metrics`
- [ ] Shadow one drift-issue triage or cost review
- [ ] First PR merged (docs fix counts — the pipeline is the lesson)

Sign-off (buddy): ______________  Date: __________
