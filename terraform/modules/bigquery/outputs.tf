output "dataset_id" {
  description = "Fully qualified dataset identifier."
  value       = google_bigquery_dataset.this.id
}

output "dataset_name" {
  description = "Dataset name."
  value       = google_bigquery_dataset.this.dataset_id
}
