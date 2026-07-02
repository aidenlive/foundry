# CLI reference

`foundry --help` for the live version; global flags: `-C/--chdir <dir>`
(run as if from another directory), `--version`.

## foundry init

Interactive-ish bootstrap for a *new* organization repo: writes
`config/foundry.yaml` and starter environment documents from answers/flags.
The shipped repo is already initialized; you'll use this when adopting
Foundry elsewhere.

## foundry validate

Schema validation + cross-document invariants (CIDR overlap, stack
references, naming pattern, secrets hygiene). Exit code 1 on any failure.
Run after every config edit; CI runs it always.

## foundry config

```bash
foundry config projects | environments
foundry config render -p <p> -e <e> [--format json|yaml] [--origins]
foundry config get    -p <p> -e <e> <dotted.path>     # value + source file
foundry config export -p <p> -e <e> --format tfvars|dotenv|backend|json|yaml
```

`get` accepts paths into the full context (`spec.` prefix optional for spec
values): `network.cidr`, `computed.name_prefix`, `kubernetes`.

## foundry stack

```bash
foundry stack init|plan|apply|destroy|output|validate \
  -p <project> -e <environment> -s <stack> \
  [--dry-run] [--allow-prod] [-- <engine args…>]
```

Renders inputs (see [Stacks](stacks.md)), then drives OpenTofu/Terraform.
Production tier requires `--allow-prod` for apply/destroy.

## foundry new

```bash
foundry new --list
foundry new <template> <dest> [--var name=value]…
```

Templates ship in `templates/`; unknown `{{ foundry.* }}` tokens are hard
errors, required variables are prompted-by-error with a clear message.

## foundry doctor

Checks the toolchain against `spec.toolchain`: python, tofu/terraform (and
minimum version), git, sops, age, provider CLIs. Optional tools report `na`
rather than an error. Always exits 0 unless `--strict` is given, in which
case a missing IaC engine fails the check (useful in CI images).

## foundry secrets

```bash
foundry secrets edit|view|encrypt|decrypt <file>
```

Thin, safe wrapper over sops (age recipients from `.sops.yaml`). `edit`
round-trips through `$EDITOR`; nothing plaintext ever touches the repo.

## foundry context

```bash
foundry context [--format text|json]
```

Machine-readable repository self-description: layout, key commands, config
model summary. Built for AI agents and new humans; `AGENTS.md` is the prose
twin.

## foundry docs

`foundry docs build` (strict) and `foundry docs serve` — wrappers over
MkDocs using the repo's `mkdocs.yml`.
