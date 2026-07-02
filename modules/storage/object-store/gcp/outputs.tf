output "bucket_id" {
  description = "Bucket identifier."
  value       = google_storage_bucket.this.id
}

output "bucket_name" {
  description = "Bucket name."
  value       = google_storage_bucket.this.name
}
