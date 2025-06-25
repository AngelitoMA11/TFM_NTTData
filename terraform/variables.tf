variable "project_id" {
  description = "ID del proyecto de GCP."
  type        = string
}
  
variable "zone" {
  description = "Zona del proyecto"
  type        = string
}

variable "region" {
  description = "Región de GCP donde se desplegarán los recursos."
  type        = string
}

variable "bq_dataset" {
  description = "Nombre del dataset de BigQuery."
  type        = string
}


variable "table_limpia" {
  description = "Nombre de la tabla de hoteles."
  type        = string
}

variable "cloud_run_service_api_streamlit" {
  description = "Nombre del servicio de Cloud Run para el servicio de datos"
  type        = string
}

variable "repository_name_api_streamlit" {
  description = "Nombre del repositorio de Artifact Registry donde está la imagen"
  type        = string
}

variable "image_name_api_streamlit" {
  description = "Nombre de la imagen de contenedor (incluye tag si aplica)"
  type        = string
}

variable "env_variables" {
  description = "Mapa de variables de entorno para el contenedor"
  type        = map(string)
  default     = {}
}