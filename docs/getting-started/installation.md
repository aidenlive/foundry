# Installation

## Requirements

| Tool                  | Version   | Notes                                   |
| --------------------- | --------- | --------------------------------------- |
| Python                | ≥ 3.10    | CLI runtime                             |
| OpenTofu or Terraform | ≥ 1.6     | `tofu` preferred, `terraform` detected  |
| git                   | any recent |                                        |
| sops + age            | optional  | only for encrypted secrets              |
| doctl / aws / gcloud / az | optional | provider CLIs for kubeconfig etc.   |

## Install

```bash
git clone https://github.com/standardcompute/foundry
cd foundry
./scripts/bootstrap.sh
source .venv/bin/activate
```

The bootstrap script creates a virtualenv, installs the CLI in editable mode
with dev extras, and runs `foundry doctor`.

## Verify

```bash
foundry --version
foundry doctor        # reports each required/optional tool
foundry validate      # validates the shipped demo configuration
```

`foundry doctor` failing on optional tools is fine — it tells you what each
one is for. Install the CLI alone (no dev extras) with
`pip install ./cli`.
