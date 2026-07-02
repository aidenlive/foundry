output "zone_id" {
  description = "Managed zone ID."
  value       = google_dns_managed_zone.this.id
}

output "name_servers" {
  description = "Delegate the domain to these name servers."
  value       = google_dns_managed_zone.this.name_servers
}
