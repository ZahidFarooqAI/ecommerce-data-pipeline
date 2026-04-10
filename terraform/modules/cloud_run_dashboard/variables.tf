variable "project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "region" {
  description = "Cloud Run region."
  type        = string
}

variable "service_name" {
  description = "Cloud Run service name."
  type        = string
}

variable "container_image" {
  description = "Full image URI for the dashboard container."
  type        = string
}

variable "container_port" {
  description = "Container port exposed by the image."
  type        = number
}

variable "allow_unauthenticated" {
  description = "Allow unauthenticated access to the service."
  type        = bool
}

variable "bigquery_dataset" {
  description = "BigQuery dataset queried by the dashboard."
  type        = string
}

variable "bigquery_aggregate_table" {
  description = "BigQuery aggregate table queried by the dashboard."
  type        = string
}

variable "labels" {
  description = "Labels applied to supported resources."
  type        = map(string)
  default     = {}
}
