data "digitalocean_kubernetes_versions" "current" {}

locals {
  version  = var.version != "" ? var.version : data.digitalocean_kubernetes_versions.current.latest_version
  tag_list = [for k, v in var.labels : "${k}:${v}"]
}

resource "digitalocean_kubernetes_cluster" "this" {
  name         = var.name
  region       = var.region
  version      = local.version
  vpc_uuid     = var.vpc_id
  ha           = var.ha_control_plane
  auto_upgrade = true
  surge_upgrade = true
  tags         = local.tag_list

  maintenance_policy {
    day        = "sunday"
    start_time = "04:00"
  }

  node_pool {
    name       = "system"
    size       = var.node_size
    auto_scale = true
    min_nodes  = var.min_nodes
    max_nodes  = var.max_nodes
    tags       = local.tag_list
  }
}
