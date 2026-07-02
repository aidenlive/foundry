resource "google_storage_bucket" "this" {
  name          = var.name
  location      = var.region
  labels        = var.labels
  force_destroy = var.force_destroy

  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"

  versioning {
    enabled = var.versioning
  }
}
