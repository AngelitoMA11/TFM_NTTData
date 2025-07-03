resource "google_storage_bucket" "chroma_bucket" {
  name          = var.bucket_name
  location      = var.region
  force_destroy = true
}

resource "google_storage_bucket_object" "modelos_llm" {
  name   = "chroma/chromadb_completa.xlsx"
  bucket = google_storage_bucket.chroma_bucket.name
  source = var.modelos_llm_path
}


