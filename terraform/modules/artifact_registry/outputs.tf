output "repository_name" {
  description = "Artifact Registry repository resource name."
  value       = google_artifact_registry_repository.this.name
}

output "repository_url" {
  description = "Repository URL prefix used for Docker image pushes."
  value       = "${google_artifact_registry_repository.this.location}-docker.pkg.dev/${google_artifact_registry_repository.this.project}/${google_artifact_registry_repository.this.repository_id}"
}
