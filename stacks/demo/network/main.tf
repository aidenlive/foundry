# Demo network stack: environment VPC on DigitalOcean.
#
# Deploy:
#   foundry stack plan  -p demo -e dev -s network
#   foundry stack apply -p demo -e dev -s network

module "labels" {
  source = "../../../modules/foundation/labels"

  org         = var.foundry_context.org.name
  project     = var.foundry_context.project.name
  environment = var.foundry_context.environment.name
  delimiter   = var.foundry_context.spec.naming.delimiter
}

module "vpc" {
  # Provider chosen in config (computed.provider = digitalocean for demo).
  source = "../../../modules/network/vpc/digitalocean"

  name   = "${module.labels.name_prefix}-vpc"
  labels = module.labels.labels
  cidr   = var.foundry_context.spec.network.cidr
  region = var.foundry_context.computed.region
}
