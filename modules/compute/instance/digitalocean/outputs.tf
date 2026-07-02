output "instance_id" {
  description = "Droplet identifier."
  value       = digitalocean_droplet.this.id
}

output "private_ip" {
  description = "Private IPv4 address inside the VPC."
  value       = digitalocean_droplet.this.ipv4_address_private
}

output "public_ip" {
  description = "Public IPv4 address (droplets always have one; exposed only when requested)."
  value       = var.public_ip ? digitalocean_droplet.this.ipv4_address : null
}
