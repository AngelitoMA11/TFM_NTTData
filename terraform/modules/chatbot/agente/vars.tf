variable "project_id" {
  description = "ID del proyecto de GCP"
  type        = string
}

variable "region" {
  description = "Región donde se desplegará el servicio"
  type        = string
}


variable "repository_name" {
  description = "Nombre del repositorio de Artifact Registry"
  type        = string
}

variable "cloud_run_service_name" {
  description = "Nombre del servicio de Cloud Run"
  type        = string
}

variable "image_name" {
  description = "Nombre de la imagen Docker (sin tag)"
  type        = string
}


variable "gemini_api_key" {
  description = "Clave de la API de Gemini (Vertex AI)"
  type        = string
}

variable "vpc_connector_id" {
  description = "ID del VPC Access Connector"
  type        = string
}
