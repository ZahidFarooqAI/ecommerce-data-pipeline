locals {
  common_labels = merge(
    {
      project     = "ecommerce-data-pipeline"
      environment = var.environment
      managed_by  = "terraform"
    },
    var.labels
  )
}

module "gcs_bucket" {
  source = "./modules/gcs_bucket"

  bucket_name = var.bucket_name
  location    = var.location
  labels      = local.common_labels
}

module "bigquery" {
  source = "./modules/bigquery"

  project_id   = var.project_id
  dataset_name = var.dataset_name
  location     = var.location
  labels       = local.common_labels
}

module "artifact_registry" {
  count  = var.create_artifact_registry ? 1 : 0
  source = "./modules/artifact_registry"

  project_id    = var.project_id
  location      = var.region
  repository_id = var.artifact_registry_repository_id
  labels        = local.common_labels
}

module "cloud_run_dashboard" {
  count  = var.deploy_dashboard ? 1 : 0
  source = "./modules/cloud_run_dashboard"

  project_id               = var.project_id
  region                   = var.region
  service_name             = var.dashboard_service_name
  container_image          = var.dashboard_container_image
  container_port           = var.dashboard_container_port
  allow_unauthenticated    = var.dashboard_allow_unauthenticated
  bigquery_dataset         = var.dataset_name
  bigquery_aggregate_table = "daily_sales_summary"
  labels                   = local.common_labels
}
