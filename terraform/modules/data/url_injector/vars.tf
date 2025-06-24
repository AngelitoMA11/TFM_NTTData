variable "project_id" {
  description = "ID del proyecto de Google Cloud"
  type        = string
}

variable "region" {
  description = "Región de despliegue de los recursos en Google Cloud"
  type        = string
}
variable "streamlit_name" {
  type        = string
  description = "Nombre del servicio Cloud Run (Agente) a actualizar"
}

variable "function_limpieza" {
  type        = string
  description = "Nombre del servicio de function para la limpieza del dataset"
}
