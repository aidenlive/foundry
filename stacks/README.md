# Stacks

A **stack** is a deployable unit of infrastructure: one Terraform/OpenTofu
root module with its own state, composed from `modules/`.

## Layout and resolution

```
stacks/<project>/<stack>/   # project-specific (checked first)
stacks/<stack>/             # shared across projects
```

`foundry stack <action> -p <project> -e <environment> -s <stack>` resolves the
directory, renders `.foundry/stack.tfvars.json` (the full config context) and
`.foundry/backend.hcl` (remote state pointer), then runs `tofu`/`terraform`.
Preview everything with `--dry-run`; production applies additionally require
`--allow-prod`.

## Conventions

1. Every stack declares exactly one context variable:

   ```hcl
   variable "foundry_context" {
     description = "Rendered Foundry configuration (injected by the CLI)."
     type        = any
   }
   ```

2. Start from `foundation/labels`, feed `name_prefix`/`labels` everywhere.
3. Pick module implementations via `computed.provider` — change the provider
   in config, update one `source` line, keep the same wiring.
4. Cross-stack references use `terraform_remote_state` against the same
   backend (see `demo/platform` for a commented example).
5. State keys follow `<org>/<project>/<environment>/<stack>.tfstate`
   automatically.
