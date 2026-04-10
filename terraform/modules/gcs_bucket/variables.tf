variable "bucket_name" {
  description = "Name of the GCS bucket."
  type        = string
}

variable "location" {
  description = "Bucket location."
  type        = string
}

variable "labels" {
  description = "Labels applied to the bucket."
  type        = map(string)
  default     = {}
}
