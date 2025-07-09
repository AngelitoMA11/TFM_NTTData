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

variable "repository_name_grafana" {
  description = "Nombre del repositorio de Artifact Registry donde está la imagen"
  type        = string
}

variable "image_name_grafana" {
  description = "ID del repositorio de Grafana en Artifact Registry"
  type        = string  
}

variable "grafana_name" {
  description = "ID del repositorio de Grafana en Artifact Registry"
  type        = string  
}

variable "user_grafana" {
  type = string
}

variable "password_grafana" {
  type = string
}
variable "vpc_network" {
  description = "Nombre de la red VPC donde se desplegarán los recursos."
  type        = string
}
variable "subnet_name" {
  description = "Nombre de la subred donde se desplegarán los recursos."
  type        = string
}

variable "cloud_run_service_api_chatbot" {
  description = "Nombre del servicio de Cloud Run para el servicio de datos"
  type        = string
}

variable "repository_name_api_chatbot" {
  description = "Nombre del repositorio de Artifact Registry donde está la imagen"
  type        = string
}

variable "image_name_api_chatbot" {
  description = "Nombre de la imagen de contenedor (incluye tag si aplica)"
  type        = string
}
variable "gemini_api_key" {
  description = "Clave de la API de Gemini (Vertex AI)"
  type        = string
}
variable "firestore_name" {
  description = "Nombre de la base de datos Firestore"
  type        = string  
}