variable "project_id" {
  description = "ID del proyecto de Google Cloud donde se creará la base de datos Firestore"
  type        = string
}

variable "name" {
  description = "Nombre de la base de datos Firestore (normalmente '(default)')"
  type        = string
  default     = "(default)"
}

variable "location_id" {
  description = "Región donde se desplegará Firestore, por ejemplo 'eur3'"
  type        = string
}

variable "type" {
  description = "Tipo de almacenamiento de Firestore: 'FIRESTORE_NATIVE' o 'DATASTORE_MODE'"
  type        = string
}