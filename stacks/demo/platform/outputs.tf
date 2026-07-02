output "cluster_name" {
  description = "DOKS cluster name (doctl kubernetes cluster kubeconfig save <name>)."
  value       = module.cluster.cluster_name
}

output "cluster_endpoint" {
  description = "Kubernetes API endpoint."
  value       = module.cluster.endpoint
}

output "artifacts_bucket" {
  description = "Spaces bucket for build artifacts."
  value       = module.artifacts.bucket_name
}
