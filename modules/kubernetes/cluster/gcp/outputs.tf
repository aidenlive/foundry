output "cluster_id" {
  description = "GKE cluster identifier."
  value       = google_container_cluster.this.id
}

output "cluster_name" {
  description = "Cluster name."
  value       = google_container_cluster.this.name
}

output "endpoint" {
  description = "API server endpoint."
  value       = google_container_cluster.this.endpoint
}

output "ca_certificate" {
  description = "Base64-encoded cluster CA certificate."
  value       = google_container_cluster.this.master_auth[0].cluster_ca_certificate
  sensitive   = true
}

output "version" {
  description = "Kubernetes master version actually running."
  value       = google_container_cluster.this.master_version
}
