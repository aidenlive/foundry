# Stacks

A stack is one deployable Terraform/OpenTofu root with its own state file.
Environments are expressed at run time (`-e`), not by copying directories —
the same stack code serves dev, staging, and prod with different injected
context.

## Resolution and layout

```
stacks/<project>/<stack>/    # project-specific, checked first
stacks/<stack>/              # shared
```

## What the CLI injects

`foundry stack <action> -p <project> -e <env> -s <stack>`:

1. Renders the context and writes
   `.foundry/stack.tfvars.json` → available as `var.foundry_context`.
2. Derives the backend from `spec.state` and writes `.foundry/backend.hcl`;
   state keys follow `<org>/<project>/<env>/<stack>.tfstate`.
3. Executes `tofu` (or `terraform`, whichever `spec.toolchain`/PATH offers):
   `init -backend-config .foundry/backend.hcl`, then the action with
   `-var-file .foundry/stack.tfvars.json`.

Flags: `--dry-run` prints commands and writes inputs without executing;
`--allow-prod` is required for apply/destroy when the environment tier is
`production`; anything after a bare `--` passes straight to the engine:

```bash
foundry stack apply -p demo -e dev -s platform -- -var vpc_id=abc123
foundry stack plan  -p demo -e prod -s network -- -detailed-exitcode
```

## Writing a stack

Scaffold: `foundry new terraform-stack stacks/<project>/<name> --var stack_name=<name>`.

Conventions (see the demo stacks for the worked example):

```hcl
variable "foundry_context" { type = any }   # the only required variable

module "labels" {
  source      = "../../../modules/foundation/labels"
  org         = var.foundry_context.org.name
  project     = var.foundry_context.project.name
  environment = var.foundry_context.environment.name
  delimiter   = var.foundry_context.spec.naming.delimiter
}
```

- Names come from `module.labels.name_prefix`; labels from
  `module.labels.labels`. No hardcoded org/project/env strings anywhere.
- Behavior differences key off config, not environment names:
  `var.foundry_context.computed.tier == "production"` — never
  `env == "prod"` string matching.
- Cross-stack values: pass explicitly with `-- -var …` while small, graduate
  to `terraform_remote_state` against the shared backend as you grow
  (commented example in `stacks/demo/platform/main.tf`).

## State

The shipped backend type is `s3`, which covers AWS S3 **and**
DigitalOcean Spaces (via `spec.state.endpoint`); `gcs` and `azurerm`
exports are supported for GCP/Azure-homed orgs. The bucket must be
versioned — the DR runbook depends on it.
