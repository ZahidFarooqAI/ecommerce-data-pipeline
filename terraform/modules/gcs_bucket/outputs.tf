output "bucket_name" {
  description = "Created bucket name."
  value       = google_storage_bucket.this.name
}
