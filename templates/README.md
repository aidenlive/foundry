# Templates

Project scaffolds rendered by `foundry new`:

```
foundry new --list
foundry new service ./services/shop --var service_name=shop
foundry new terraform-stack ./stacks/demo/dns --var stack_name=dns
foundry new static-site ./sites/status
```

## Authoring templates

A template is a directory with a `template.yaml` manifest:

```yaml
name: service
description: Production-ready HTTP service
variables:
  - name: service_name
    description: DNS-safe service name
    required: true
  - name: port
    default: 8080
```

Rendering rules:

- `{{ foundry.<var> }}` in file contents is substituted; unknown variables
  are a hard error (typos fail fast, nothing ships half-rendered).
- `__var__` path segments are substituted in file and directory names.
- GitHub Actions expressions (`${{ ... }}`) pass through untouched — the
  `foundry.` prefix is what marks a Foundry token.
- Built-ins available everywhere: `name` (destination basename), `year`,
  `org`, `org_domain`, `org_repository`.
- Binary files are copied verbatim; file modes are preserved.
