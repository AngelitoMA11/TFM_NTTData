# Crear cuenta de servicio para Grafana
resource "google_service_account" "grafana" {
  account_id   = "grafana-sa"
  display_name = "Grafana Cloud Run Service Account"
}

resource "google_project_iam_member" "grafana_bigquery_reader" {
  project = var.project_id
  role    = "roles/bigquery.dataViewer"
  member  = "serviceAccount:${google_service_account.grafana.email}"
}

resource "google_project_iam_member" "grafana_bigquery_access" {
  project = var.project_id
  role    = "roles/bigquery.user"
  member  = "serviceAccount:${google_service_account.grafana.email}"
}

resource "null_resource" "docker_auth" {
  provisioner "local-exec" {
    command = "gcloud auth configure-docker ${var.region}-docker.pkg.dev"
  }
}

resource "null_resource" "build_push_image" {
    triggers = {
    always_run = "${timestamp()}"
  } 
  provisioner "local-exec" {
    command = <<EOT
        docker build --platform=linux/amd64 -t ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/${var.image_name}:latest ${path.module}/docker && docker push ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/${var.image_name}:latest 
    EOT
  }
  depends_on = [null_resource.docker_auth]
}

resource "google_cloud_run_v2_service" "grafana" {
  name     = var.grafana_name
  location = var.region
  deletion_protection = false

  template {
    service_account = google_service_account.grafana.email
      containers {
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_id}/${var.image_name}:latest"
        ports {
          container_port = 3000
        }
        env {
          name  = "GF_SECURITY_ADMIN_USER"
          value = var.user_grafana
        }

        env {
          name  = "GF_SECURITY_ADMIN_PASSWORD"
          value = var.password_grafana
        }
      }
    
  }

  traffic {
    type = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }

    depends_on = [ null_resource.build_push_image ]
}

resource "google_cloud_run_service_iam_member" "grafana_invoker" {
  service  = google_cloud_run_v2_service.grafana.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"
}
