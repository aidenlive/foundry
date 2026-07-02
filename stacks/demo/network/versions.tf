terraform {
  required_version = ">= 1.6.0"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = ">= 2.30"
    }
  }

  # Remote state is injected by the CLI:
  #   foundry stack init -p demo -e dev -s network
  # writes .foundry/backend.hcl from spec.state and passes it via
  # -backend-config. Uncomment to pin the backend type explicitly:
  #
  # backend "s3" {}
}
