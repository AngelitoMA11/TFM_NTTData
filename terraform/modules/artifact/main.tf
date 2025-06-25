resource "google_artifact_registry_repository" "repos" {
  for_each     = toset(var.repo_names)
  project      = var.project_id
  location     = var.region
  repository_id = each.key
  format       = "DOCKER"
}