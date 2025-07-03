variable "name" {
  description = "Nombre del VPC Access Connector"
  type        = string
}

variable "region" {
  description = "Región donde se desplegará el conector"
  type        = string
}

variable "vpc_network" {
  description = "Nombre de la VPC a la que se conectará"
  type        = string
}
variable "subnet_name" {
  description = "Nombre de la subred a utilizar"
  type        = string
  default     = "rag-subnet"
  
}

variable "cidr_range" {
  description = "Rango CIDR para el VPC Access Connector"
  type        = string
}
