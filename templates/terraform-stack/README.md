# {{ foundry.stack_name }} stack

Scaffolded by `foundry new terraform-stack` for {{ foundry.org }}.

```
foundry stack plan  -p <project> -e <environment> -s {{ foundry.stack_name }}
foundry stack apply -p <project> -e <environment> -s {{ foundry.stack_name }}
```

The CLI injects `var.foundry_context` (full rendered config) and the remote
state backend; see `stacks/README.md` for conventions. Add modules from
`modules/<capability>/<component>/{{ foundry.provider }}` and keep the labels
module as the naming source of truth.
