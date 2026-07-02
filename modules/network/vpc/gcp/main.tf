resource "google_compute_network" "this" {
  name                    = var.name
  auto_create_subnetworks = false
  routing_mode            = "REGIONAL"
}

resource "google_compute_subnetwork" "public" {
  count = length(var.public_subnets)

  name          = "${var.name}-public-${count.index}"
  network       = google_compute_network.this.id
  region        = var.region
  ip_cidr_range = var.public_subnets[count.index]
}

resource "google_compute_subnetwork" "private" {
  count = length(var.private_subnets)

  name                     = "${var.name}-private-${count.index}"
  network                  = google_compute_network.this.id
  region                   = var.region
  ip_cidr_range            = var.private_subnets[count.index]
  private_ip_google_access = true
}

resource "google_compute_router" "this" {
  count = var.enable_nat ? 1 : 0

  name    = "${var.name}-router"
  network = google_compute_network.this.id
  region  = var.region
}

resource "google_compute_router_nat" "this" {
  count = var.enable_nat ? 1 : 0

  name                               = "${var.name}-nat"
  router                             = google_compute_router.this[0].name
  region                             = var.region
  nat_ip_allocate_option             = "AUTO_ONLY"
  source_subnetwork_ip_ranges_to_nat = "ALL_SUBNETWORKS_ALL_IP_RANGES"
}

# Default-deny posture: GCP networks have no implicit allow rules beyond the
# implied egress; internal traffic must be opened explicitly per environment.
resource "google_compute_firewall" "deny_all_ingress" {
  name      = "${var.name}-deny-all-ingress"
  network   = google_compute_network.this.id
  direction = "INGRESS"
  priority  = 65534

  deny {
    protocol = "all"
  }

  source_ranges = ["0.0.0.0/0"]
}
