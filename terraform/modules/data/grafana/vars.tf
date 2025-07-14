variable "project_id" {
  description = "ID del proyecto de Google Cloud donde se desplegará Grafana"
  type        = string
}

variable "region" {
  description = "Región de Google Cloud para el despliegue de Grafana"
  type        = string
}

variable "user_grafana" {
  description = "Usuario administrador para Grafana"
  type        = string
}

variable "password_grafana" {
  description = "Contraseña para el usuario administrador de Grafana"
  type        = string
}

variable "repository_id" {
  description = "ID del repositorio de artefactos para la imagen de Grafana"
  type        = string
}

variable "grafana_name" {
  description = "Nombre del recurso de Grafana"
  type        = string
}

variable "image_name" {
  description = "Nombre de la imagen de Docker para Grafana"
  type        = string
}