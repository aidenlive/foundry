output "zone_id" {
  description = "Domain identifier (urn)."
  value       = digitalocean_domain.this.urn
}

output "name_servers" {
  description = "DigitalOcean uses a static name server set for all domains."
  value       = ["ns1.digitalocean.com", "ns2.digitalocean.com", "ns3.digitalocean.com"]
}
