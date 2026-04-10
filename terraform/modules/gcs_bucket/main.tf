resource "google_storage_bucket" "this" {
  name                        = var.bucket_name
  location                    = var.location
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  labels = var.labels

  versioning {
    enabled = true
  }
}
