resource "digitalocean_vpc" "this" {
  name        = var.name
  region      = var.region
  ip_range    = var.cidr
  description = "Managed by Foundry (${lookup(var.labels, "environment", "unspecified")})"
}
