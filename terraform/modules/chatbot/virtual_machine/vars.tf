variable "project_id" {
  description = "ID del proyecto de GCP"
  type        = string
}

variable "region" {
  description = "Región de la VM"
  type        = string
}

variable "zone" {
  description = "Zona donde se desplegará la VM"
  type        = string
}

variable "vm_name" {
  description = "Nombre de la máquina virtual"
  type        = string
}

variable "vm_machine_type" {
  description = "Tipo de máquina (ej. n2-standard-2)"
  type        = string
}

variable "disk_size_gb" {
  description = "Tamaño del disco adicional en GB"
  type        = number
}

variable "startup_script" {
  description = "Script de arranque para configurar la VM"
  type        = string
}

variable "vpc_network" {
  description = "Nombre de la red VPC donde se conecta la VM"
  type        = string
}

variable "subnet" {
  description = "Nombre de la subred donde se conecta la VM"
  type        = string
}
