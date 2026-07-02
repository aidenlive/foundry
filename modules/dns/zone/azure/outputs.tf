output "zone_id" {
  description = "DNS zone ID."
  value       = azurerm_dns_zone.this.id
}

output "name_servers" {
  description = "Delegate the domain to these name servers."
  value       = azurerm_dns_zone.this.name_servers
}
