variable "project_id" {
  description = "Google Cloud project ID used by the ecommerce data pipeline."
  type        = string
}

variable "region" {
  description = "Default Google Cloud region for regional resources."
  type        = string
  default     = "us-central1"
}

variable "location" {
  description = "Location for multi-region resources such as GCS and BigQuery."
  type        = string
  default     = "US"
}

variable "bucket_name" {
  description = "Name of the GCS bucket used as the data lake."
  type        = string
}

variable "dataset_name" {
  description = "BigQuery dataset name used by the pipeline."
  type        = string
  default     = "ecommerce"
}

variable "environment" {
  description = "Environment label used for resource tagging."
  type        = string
  default     = "dev"
}

variable "labels" {
  description = "Additional labels to apply to supported resources."
  type        = map(string)
  default     = {}
}

variable "create_artifact_registry" {
  description = "Whether to create an Artifact Registry repository for Docker images."
  type        = bool
  default     = true
}

variable "artifact_registry_repository_id" {
  description = "Artifact Registry repository ID used for dashboard images."
  type        = string
  default     = "ecommerce-dashboard"
}

variable "deploy_dashboard" {
  description = "Whether to deploy the Streamlit dashboard to Cloud Run."
  type        = bool
  default     = false
}

variable "dashboard_service_name" {
  description = "Cloud Run service name for the dashboard."
  type        = string
  default     = "ecommerce-dashboard"
}

variable "dashboard_container_image" {
  description = "Full container image URI for the dashboard deployment."
  type        = string
  default     = ""
}

variable "dashboard_container_port" {
  description = "Container port exposed by the dashboard image."
  type        = number
  default     = 8080
}

variable "dashboard_allow_unauthenticated" {
  description = "Allow public access to the dashboard Cloud Run service."
  type        = bool
  default     = true
}
