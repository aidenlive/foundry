output "instance_id" {
  description = "Virtual machine identifier."
  value       = azurerm_linux_virtual_machine.this.id
}

output "private_ip" {
  description = "Primary private IPv4 address."
  value       = azurerm_network_interface.this.private_ip_address
}

output "public_ip" {
  description = "Public IPv4 address, or null when public_ip = false."
  value       = var.public_ip ? azurerm_public_ip.this[0].ip_address : null
}
