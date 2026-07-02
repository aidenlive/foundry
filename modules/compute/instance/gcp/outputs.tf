output "instance_id" {
  description = "Instance identifier."
  value       = google_compute_instance.this.id
}

output "private_ip" {
  description = "Primary internal IP."
  value       = google_compute_instance.this.network_interface[0].network_ip
}

output "public_ip" {
  description = "External IP, or null when public_ip = false."
  value       = var.public_ip ? google_compute_instance.this.network_interface[0].access_config[0].nat_ip : null
}
