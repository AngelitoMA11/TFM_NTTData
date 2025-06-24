output "function_limpieza_url" {
  value = google_cloudfunctions2_function.function_limpieza.service_config[0].uri
  description = "Function para la limpieza del dataset"
}