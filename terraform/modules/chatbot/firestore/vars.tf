variable "project_id" {
  type = string
}

variable "name" {
  type    = string
  default = "(default)"
}

variable "location_id" {
  type = string
}

variable "type" {
  type = string
  description = "Firestore type: NATIVE_MODE or DATASTORE_MODE"
}
