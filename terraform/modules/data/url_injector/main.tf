resource "null_resource" "update-cloud-function" {

  provisioner "local-exec" {
      command = <<EOT
      gcloud run services update ${var.streamlit_name} --region=${var.region} --project=${var.project_id} --update-env-vars=FUNCTION_LIMPIEZA=${var.function_limpieza}  
  EOT
    }
}
