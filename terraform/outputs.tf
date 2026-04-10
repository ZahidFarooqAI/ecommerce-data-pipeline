output "gcs_bucket_name" {
  description = "Name of the provisioned GCS bucket."
  value       = module.gcs_bucket.bucket_name
}

output "bigquery_dataset_id" {
  description = "Fully qualified BigQuery dataset ID."
  value       = module.bigquery.dataset_id
}

output "pipeline_config_hint" {
  description = "Values to copy into src/config.py after provisioning."
  value = {
    GCS_BUCKET       = module.gcs_bucket.bucket_name
    BIGQUERY_PROJECT = var.project_id
    BIGQUERY_DATASET = module.bigquery.dataset_name
  }
}

output "artifact_registry_repository" {
  description = "Artifact Registry repository for Docker images, if enabled."
  value       = var.create_artifact_registry ? module.artifact_registry[0].repository_name : null
}

output "artifact_registry_repository_url" {
  description = "Artifact Registry repository URL prefix for Docker pushes, if enabled."
  value       = var.create_artifact_registry ? module.artifact_registry[0].repository_url : null
}

output "cloud_run_dashboard_url" {
  description = "Cloud Run dashboard URL, if deployment is enabled."
  value       = var.deploy_dashboard ? module.cloud_run_dashboard[0].service_url : null
}
