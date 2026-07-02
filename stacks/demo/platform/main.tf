# Demo platform stack: DOKS cluster + Spaces bucket inside the demo VPC.
#
# Order matters: apply demo/network first, then pass its vpc_id here
# (or wire the terraform_remote_state lookup below to the shared backend).

module "labels" {
  source = "../../../modules/foundation/labels"

  org         = var.foundry_context.org.name
  project     = var.foundry_context.project.name
  environment = var.foundry_context.environment.name
  delimiter   = var.foundry_context.spec.naming.delimiter
}

# Cross-stack input, option A (explicit, great for getting started):
#   foundry stack apply -p demo -e dev -s platform -- -var vpc_id=<uuid>
#
# Option B (automatic, once remote state is configured):
#
# data "terraform_remote_state" "network" {
#   backend = "s3"
#   config = {
#     bucket   = var.foundry_context.spec.state.bucket
#     key      = "${var.foundry_context.computed.state_key_prefix}/network.tfstate"
#     region   = var.foundry_context.spec.state.region
#     endpoint = var.foundry_context.spec.state.endpoint
#   }
# }
# locals { vpc_id = data.terraform_remote_state.network.outputs.vpc_id }

module "cluster" {
  source = "../../../modules/kubernetes/cluster/digitalocean"

  name      = "${module.labels.name_prefix}-k8s"
  labels    = module.labels.labels
  region    = var.foundry_context.computed.region
  node_size = var.foundry_context.spec.kubernetes.nodeSize
  min_nodes = var.foundry_context.spec.kubernetes.minNodes
  max_nodes = var.foundry_context.spec.kubernetes.maxNodes
  vpc_id    = var.vpc_id

  ha_control_plane = var.foundry_context.computed.tier == "production"
}

module "artifacts" {
  source = "../../../modules/storage/object-store/digitalocean"

  name       = "${module.labels.name_prefix}-artifacts"
  labels     = module.labels.labels
  region     = var.foundry_context.computed.region
  versioning = true
}
