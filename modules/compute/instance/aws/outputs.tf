output "instance_id" {
  description = "EC2 instance ID."
  value       = aws_instance.this.id
}

output "private_ip" {
  description = "Primary private IPv4 address."
  value       = aws_instance.this.private_ip
}

output "public_ip" {
  description = "Public IPv4 address, or null when public_ip = false."
  value       = aws_instance.this.public_ip
}
