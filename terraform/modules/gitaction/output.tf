data "google_project" "project" {
  project_id = var.project_id
}

output "workload_identity_provider" {
  description = "Nombre completo del Workload Identity Provider"
  value       = "projects/${data.google_project.project.number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.github.workload_identity_pool_id}/providers/${google_iam_workload_identity_pool_provider.github.workload_identity_pool_provider_id}"
}

output "service_account_email" {
  description = "Email de la Service Account que usará GitHub"
  value       = google_service_account.github_ci.email
}