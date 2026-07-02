output "cluster_id" {
  description = "EKS cluster identifier."
  value       = aws_eks_cluster.this.id
}

output "cluster_name" {
  description = "Cluster name."
  value       = aws_eks_cluster.this.name
}

output "endpoint" {
  description = "API server endpoint."
  value       = aws_eks_cluster.this.endpoint
}

output "ca_certificate" {
  description = "Base64-encoded cluster CA certificate."
  value       = aws_eks_cluster.this.certificate_authority[0].data
  sensitive   = true
}

output "version" {
  description = "Kubernetes version actually running."
  value       = aws_eks_cluster.this.version
}
