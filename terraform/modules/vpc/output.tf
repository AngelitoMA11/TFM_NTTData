output "connector_id" {
  description = "ID del VPC Access Connector"
  value       = google_vpc_access_connector.connector.id
}

output "connector_name" {
  description = "Nombre del VPC Access Connector"
  value       = google_vpc_access_connector.connector.name
}

output "subnet_id" {
  value = google_compute_subnetwork.rag_subnet.id
}