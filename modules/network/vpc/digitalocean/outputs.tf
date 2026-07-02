output "vpc_id" {
  description = "VPC identifier."
  value       = digitalocean_vpc.this.id
}

output "public_subnet_ids" {
  description = "Always empty: DigitalOcean VPCs have no subnet primitive."
  value       = []
}

output "private_subnet_ids" {
  description = "Always empty: DigitalOcean VPCs have no subnet primitive."
  value       = []
}
