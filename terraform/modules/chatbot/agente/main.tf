# Autenticación con Artifact Registry
resource "null_resource" "docker_auth" {
  provisioner "local-exec" {
    command = "gcloud auth configure-docker ${var.region}-docker.pkg.dev"
  }

}

# Construcción de la imagen con Docker y push a Artifact Registry
resource "null_resource" "build_push_image" {
    triggers = {
    always_run = "${timestamp()}"
  } 
  provisioner "local-exec" {
    command = <<EOT
        docker build --platform=linux/amd64 -t ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_name}/${var.image_name}:latest ${path.module}/../../../../chatbot/cloud_run_agente && docker push ${var.region}-docker.pkg.dev/${var.project_id}/${var.repository_name}/${var.image_name}:latest 
    EOT
  }
  depends_on = [null_resource.docker_auth]
}


resource "google_cloud_run_v2_service" "agente" {
  name     = var.cloud_run_service_name
  location = var.region
  project  = var.project_id
  deletion_protection = false
  
  template {
      containers {
        image = "europe-west1-docker.pkg.dev/${var.project_id}/${var.repository_name}/${var.image_name}:latest"

        env {
          name  = "CHROMA_HOST"
          value = ""
        }

        env {
          name  = "CHROMA_PORT"
          value = "8080"
        }

        env {
          name  = "GOOGLE_PROJECT_ID"
          value = var.project_id
        }

        env {
          name  = "GEMINI_API_KEY"
          value = var.gemini_api_key
        }
        
        ports {
            container_port = 8000
        }
      }
    
      vpc_access {
        connector = var.vpc_connector_id
        egress    = "ALL_TRAFFIC"
      }
  }

  traffic {
    type = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
    percent = 100
  }
}

resource "google_cloud_run_service_iam_member" "allow_all" {
  location = var.region
  project  = var.project_id
  service  = google_cloud_run_v2_service.agente.name
  role   = "roles/run.invoker"
  member = "allUsers"
}