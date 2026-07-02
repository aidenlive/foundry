# Changelog

All notable changes to Foundry are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project
adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-07-01

### Added

- Configuration model: `Organization` / `Project` / `Environment` documents
  with layered precedence, JSON Schema validation, and per-value provenance.
- `foundry` CLI: `init`, `validate`, `config` (render/get/export/projects/
  environments), `new`, `stack`, `doctor`, `context`, `secrets`, `docs`.
- Cloud-agnostic module contracts with AWS, GCP, Azure, and DigitalOcean
  implementations: `network/vpc`, `compute/instance`, `kubernetes/cluster`,
  `storage/object-store`, `dns/zone`, plus provider-free `foundation/labels`.
- Demo project: DigitalOcean network + platform (DOKS, Spaces) stacks.
- Templates: `service`, `terraform-stack`, `static-site`.
- GitHub automation: CI, docs deploy, releases, reusable stack pipeline with
  environment protection, nightly drift detection.
- Operational runbooks, checklists, MkDocs documentation site, `AGENTS.md`,
  `docs/llms.txt`, and machine-readable `foundry context`.
