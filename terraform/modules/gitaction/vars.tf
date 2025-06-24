variable "project_id" {
  type = string
}

variable "wif_pool_name" {
  type    = string
  default = "github-pool"
}

variable "wif_provider_id" {
  type    = string
  default = "github-provider"
}

variable "github_repo" {
  type = string
  description = "Ejemplo: tuusuario/turepo"
}

variable "service_account_id" {
  type    = string
  default = "github-ci"
}

variable "service_account_role" {
  type    = string
  default = "roles/editor"
}
variable "region" {
  
}