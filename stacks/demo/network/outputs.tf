output "vpc_id" {
  description = "Environment VPC identifier, consumed by the platform stack."
  value       = module.vpc.vpc_id
}

output "name_prefix" {
  description = "Canonical name prefix for downstream stacks."
  value       = module.labels.name_prefix
}
