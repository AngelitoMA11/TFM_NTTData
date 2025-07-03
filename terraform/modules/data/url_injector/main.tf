resource "null_resource" "update-streamlit" {

  provisioner "local-exec" {
      command = <<EOT
      gcloud run services update ${var.streamlit_name} --region=${var.region} --project=${var.project_id} --update-env-vars=FUNCTION_LIMPIEZA=${var.function_limpieza} --update-env-vars=AGENT_URL=${var.agent_url}    
  EOT
    }
}

resource "null_resource" "update-api-agente" {

  provisioner "local-exec" {
      command = <<EOT
      gcloud run services update ${var.agente_name} --region=${var.region} --project=${var.project_id} --update-env-vars=CHROMA_HOST=${var.chroma_host}  
  EOT
    }
}

