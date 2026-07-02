output "bucket_id" {
  description = "Bucket identifier."
  value       = aws_s3_bucket.this.id
}

output "bucket_name" {
  description = "Bucket name."
  value       = aws_s3_bucket.this.bucket
}
