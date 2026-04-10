variable "project_id" {
  description = "Google Cloud project ID."
  type        = string
}

variable "dataset_name" {
  description = "BigQuery dataset name."
  type        = string
}

variable "location" {
  description = "Dataset location."
  type        = string
}

variable "labels" {
  description = "Labels applied to the dataset."
  type        = map(string)
  default     = {}
}
