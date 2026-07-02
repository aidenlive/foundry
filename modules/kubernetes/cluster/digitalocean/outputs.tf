output "cluster_id" {
  description = "DOKS cluster identifier."
  value       = digitalocean_kubernetes_cluster.this.id
}

output "cluster_name" {
  description = "Cluster name."
  value       = digitalocean_kubernetes_cluster.this.name
}

output "endpoint" {
  description = "API server endpoint."
  value       = digitalocean_kubernetes_cluster.this.endpoint
}

output "ca_certificate" {
  description = "Base64-encoded cluster CA certificate."
  value       = digitalocean_kubernetes_cluster.this.kube_config[0].cluster_ca_certificate
  sensitive   = true
}

output "version" {
  description = "Kubernetes version actually running."
  value       = digitalocean_kubernetes_cluster.this.version
}
