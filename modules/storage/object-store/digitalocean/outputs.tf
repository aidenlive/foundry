output "bucket_id" {
  description = "Bucket identifier (urn)."
  value       = digitalocean_spaces_bucket.this.urn
}

output "bucket_name" {
  description = "Bucket name."
  value       = digitalocean_spaces_bucket.this.name
}
