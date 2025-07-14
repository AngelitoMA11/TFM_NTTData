provider "google" {
  project = var.project_id
  region  = var.region
  zone    = var.zone
}

terraform {
  required_version = "1.10.4"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "= 6.43.0"
    }
  }

}