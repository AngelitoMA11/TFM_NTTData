variable "name" {
  description = "Nombre de la función Cloud Function."
  type        = string
}

variable "entry_point" {
  description = "Nombre del método principal que se ejecuta en la función."
  type        = string
}

variable "env_variables" {
  description = "Variables de entorno para la función."
  type        = map(string)
}

variable "project_id" {
  description = "ID del proyecto de GCP."
  type        = string
}

variable "region" {
  description = "Región de GCP donde se desplegarán los recursos."
  type        = string
}