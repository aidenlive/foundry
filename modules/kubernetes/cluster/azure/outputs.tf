output "cluster_id" {
  description = "AKS cluster identifier."
  value       = azurerm_kubernetes_cluster.this.id
}

output "cluster_name" {
  description = "Cluster name."
  value       = azurerm_kubernetes_cluster.this.name
}

output "endpoint" {
  description = "API server endpoint."
  value       = azurerm_kubernetes_cluster.this.kube_config[0].host
  sensitive   = true
}

output "ca_certificate" {
  description = "Base64-encoded cluster CA certificate."
  value       = azurerm_kubernetes_cluster.this.kube_config[0].cluster_ca_certificate
  sensitive   = true
}

output "version" {
  description = "Kubernetes version actually running."
  value       = azurerm_kubernetes_cluster.this.kubernetes_version
}
