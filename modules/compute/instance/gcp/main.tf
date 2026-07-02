locals {
  zone = var.zone != "" ? var.zone : "${var.region}-a"
  metadata_base = {
    block-project-ssh-keys = "true"
  }
  metadata_ssh = var.ssh_public_key != "" ? { ssh-keys = "ubuntu:${var.ssh_public_key}" } : {}
  metadata_ud  = var.user_data != "" ? { user-data = var.user_data } : {}
}

resource "google_compute_instance" "this" {
  name         = var.name
  machine_type = var.size
  zone         = local.zone
  labels       = var.labels

  boot_disk {
    initialize_params {
      image = var.image
      size  = var.root_volume_gb
      type  = "pd-balanced"
    }
  }

  # Google-managed encryption at rest is always on for persistent disks.
  network_interface {
    subnetwork = var.subnet_id

    dynamic "access_config" {
      for_each = var.public_ip ? [1] : []
      content {}
    }
  }

  metadata = merge(local.metadata_base, local.metadata_ssh, local.metadata_ud)

  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }
}
