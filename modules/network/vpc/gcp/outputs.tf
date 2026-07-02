output "vpc_id" {
  description = "Network identifier (self_link)."
  value       = google_compute_network.this.id
}

output "public_subnet_ids" {
  description = "IDs of public subnetworks."
  value       = google_compute_subnetwork.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnetworks."
  value       = google_compute_subnetwork.private[*].id
}
