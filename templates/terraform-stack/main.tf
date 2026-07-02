# Stack: {{ foundry.stack_name }} (scaffolded by foundry new, {{ foundry.year }})

module "labels" {
  source = "../../../modules/foundation/labels"

  org         = var.foundry_context.org.name
  project     = var.foundry_context.project.name
  environment = var.foundry_context.environment.name
  delimiter   = var.foundry_context.spec.naming.delimiter
}

# Add infrastructure below. Example:
#
# module "vpc" {
#   source = "../../../modules/network/vpc/{{ foundry.provider }}"
#
#   name   = "${module.labels.name_prefix}-vpc"
#   labels = module.labels.labels
#   cidr   = var.foundry_context.spec.network.cidr
#   region = var.foundry_context.computed.region
# }
