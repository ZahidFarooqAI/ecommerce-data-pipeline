resource "google_service_account" "dashboard" {
  account_id   = substr(replace("${var.service_name}-sa", "_", "-"), 0, 30)
  display_name = "Dashboard Cloud Run service account"
  project      = var.project_id
}

resource "google_project_iam_member" "bigquery_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.dashboard.email}"
}

resource "google_bigquery_dataset_iam_member" "dataset_viewer" {
  project    = var.project_id
  dataset_id = var.bigquery_dataset
  role       = "roles/bigquery.dataViewer"
  member     = "serviceAccount:${google_service_account.dashboard.email}"
}

resource "google_cloud_run_v2_service" "this" {
  name     = var.service_name
  location = var.region
  project  = var.project_id

  template {
    service_account = google_service_account.dashboard.email

    containers {
      image = var.container_image

      ports {
        container_port = var.container_port
      }

      env {
        name  = "PORT"
        value = tostring(var.container_port)
      }

      env {
        name  = "DASHBOARD_DATA_SOURCE"
        value = "bigquery"
      }

      env {
        name  = "BIGQUERY_PROJECT"
        value = var.project_id
      }

      env {
        name  = "BIGQUERY_DATASET"
        value = var.bigquery_dataset
      }

      env {
        name  = "BIGQUERY_AGG_TABLE"
        value = var.bigquery_aggregate_table
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "public_invoker" {
  count    = var.allow_unauthenticated ? 1 : 0
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.this.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
