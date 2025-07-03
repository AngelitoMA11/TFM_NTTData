variable "bucket_name" {
  description = "Nombre del bucket de GCS donde se subirán los archivos"
  type        = string
}

variable "region" {
  description = "Región donde se creará el bucket"
  type        = string
}

variable "modelos_llm_path" {
  description = "Ruta local del archivo modelos_llm.csv"
  type        = string
}
