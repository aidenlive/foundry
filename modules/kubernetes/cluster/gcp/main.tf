resource "google_container_cluster" "this" {
  name     = var.name
  location = var.region

  network    = var.vpc_id
  subnetwork = length(var.subnet_ids) > 0 ? var.subnet_ids[0] : null

  # We manage our own pool; the default pool is created then removed.
  remove_default_node_pool = true
  initial_node_count       = 1
  deletion_protection      = false

  min_master_version = var.version != "" ? var.version : null

  release_channel {
    channel = var.version != "" ? "UNSPECIFIED" : "REGULAR"
  }

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  resource_labels = var.labels
}

resource "google_container_node_pool" "system" {
  name     = "${var.name}-system"
  cluster  = google_container_cluster.this.id
  location = var.region

  autoscaling {
    min_node_count = var.min_nodes
    max_node_count = var.max_nodes
  }

  management {
    auto_repair  = true
    auto_upgrade = true
  }

  node_config {
    machine_type = var.node_size
    disk_type    = "pd-balanced"
    disk_size_gb = 50
    labels       = var.labels

    workload_metadata_config {
      mode = "GKE_METADATA"
    }

    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]
  }
}
