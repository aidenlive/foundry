resource "google_dns_managed_zone" "this" {
  name     = replace(var.name, ".", "-")
  dns_name = "${var.name}."
  labels   = var.labels

  dnssec_config {
    state = "on"
  }
}
