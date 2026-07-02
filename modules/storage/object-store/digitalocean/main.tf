resource "digitalocean_spaces_bucket" "this" {
  name          = var.name
  region        = var.region
  acl           = "private"
  force_destroy = var.force_destroy

  versioning {
    enabled = var.versioning
  }
}
