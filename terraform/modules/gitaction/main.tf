provider "google-beta" {
  project = var.project_id
  region  = var.region
}

resource "google_service_account" "github_ci" {
  account_id   = var.service_account_id
  display_name = "GitHub CI Service Account"
}

resource "google_project_iam_member" "github_ci_permissions" {
  project = var.project_id
  role    = var.service_account_role
  member  = "serviceAccount:${google_service_account.github_ci.email}"
}

resource "google_iam_workload_identity_pool" "github" {
  provider                  = google-beta
  workload_identity_pool_id = var.wif_pool_name
  display_name              = "GitHub Pool"
  description               = "Permite a GitHub Actions autenticarse vía OIDC"
}

resource "google_iam_workload_identity_pool_provider" "github" {
  provider                            = google-beta
  workload_identity_pool_id           = google_iam_workload_identity_pool.github.workload_identity_pool_id
  workload_identity_pool_provider_id  = var.wif_provider_id
  display_name                        = "GitHub OIDC Provider"

  oidc {
    issuer_uri = "https://token.actions.githubusercontent.com"
  }

  attribute_mapping = {
    "google.subject"       = "assertion.sub"
    "attribute.repository" = "assertion.repository"
    "attribute.actor"      = "assertion.actor"
  }

  attribute_condition = "attribute.repository == \"${var.github_repo}\""
}

resource "google_service_account_iam_member" "wif_binding" {
  service_account_id = google_service_account.github_ci.name
  role               = "roles/iam.workloadIdentityUser"
  member             = "principalSet://iam.googleapis.com/${google_iam_workload_identity_pool.github.name}/attribute.repository/${var.github_repo}"
}
