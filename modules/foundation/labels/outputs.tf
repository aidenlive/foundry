output "name_prefix" {
  description = "Canonical <org>-<project>-<environment> prefix."
  value       = local.prefix
}

output "labels" {
  description = "Base Foundry labels merged with extra_labels."
  value       = local.labels
}

output "delimiter" {
  description = "Delimiter, re-exported for name composition in stacks."
  value       = local.delimiter
}
