output "vpc_id" {
  description = "Virtual network identifier."
  value       = azurerm_virtual_network.this.id
}

output "public_subnet_ids" {
  description = "IDs of public subnets."
  value       = azurerm_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "IDs of private subnets."
  value       = azurerm_subnet.private[*].id
}

output "resource_group_name" {
  description = "Resource group used by the network (created or pre-existing)."
  value       = local.resource_group_name
}
