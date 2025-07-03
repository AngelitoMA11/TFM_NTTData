output "api_agente_url" {
  value       = google_cloud_run_v2_service.agente.uri
  description = "URL pública del servicio Cloud Run api-data"
}
output "api_agente_name" {
  description = "Nombre del servicio Cloud Run apiagent"
  value       = google_cloud_run_v2_service.agente.name
}
