variable "project_id" {
  description = "ID del proyecto de Google Cloud donde se desplegarán los artefactos"
  type        = string
}

variable "region" {
  description = "Región de Google Cloud donde se desplegarán los recursos"
  type        = string
}

variable "repo_names" {
  description = "Lista de nombres de los repositorios de artefactos"
  type        = list(string)
}