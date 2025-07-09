resource "google_firestore_database" "default" {
  name                       = var.name
  project                    = var.project_id
  location_id                = var.location_id
  type                       = var.type  
  delete_protection_state    = "DELETE_PROTECTION_DISABLED"
  lifecycle {
    prevent_destroy = true
  }
}
