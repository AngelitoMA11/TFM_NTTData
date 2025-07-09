terraform {
  backend "gcs" {
    bucket  = "tfm-bucket-nttdata"
    prefix  = "estado" 
  }
}


module "bigquery" {
  source     = "./modules/data/bigquery"
  project_id = var.project_id
  bq_dataset = var.bq_dataset
  
  tables = [
    { name = var.table_limpia, schema = "schemas/metricas.json" },
  ]
}

module "artifact" {
  source      = "./modules/artifact"
  project_id  = var.project_id
  region      = var.region
  repo_names  = [var.repository_name_api_streamlit, var.repository_name_grafana, var.repository_name_api_chatbot]
}

module "function_limpieza" {
  source = "./modules/data/function_limpieza"
  project_id     = var.project_id
  region         = var.region
  name           = "limpieza"
  entry_point    = "main"
  env_variables  = {
    PROJECT_ID     = var.project_id
    DATASET        = var.bq_dataset
    TABLE          = var.table_limpia
  }
}

module "streamlit" {
  source                 = "./modules/streamlit"
  project_id             = var.project_id
  region                 = var.region
  cloud_run_service_name = var.cloud_run_service_api_streamlit
  repository_name        = var.repository_name_api_streamlit
  image_name             = var.image_name_api_streamlit
  firestore_database     = var.firestore_name
  depends_on             = [module.artifact]
}

module "injector" {
  source             = "./modules/data/url_injector"
  project_id         = var.project_id
  region             = var.region
  streamlit_name     = module.streamlit.streamlit_name
  agente_name        = module.chatbot.api_agente_name
  agent_url          = module.chatbot.api_agente_url
  chroma_host        = module.chroma_vm.chroma_vm_internal_ip
  function_limpieza  = module.function_limpieza.function_limpieza_url
  depends_on         = [module.streamlit, module.function_limpieza, module.chroma_vm, module.gcs_datos, module.vpc_connector, module.chatbot]
}

module "grafana" {
  source           = "./modules/data/grafana"
  project_id       = var.project_id
  region           = var.region
  password_grafana = var.password_grafana
  user_grafana     = var.user_grafana
  repository_id    = var.repository_name_grafana
  grafana_name     = var.grafana_name
  image_name       = var.image_name_grafana

  depends_on = [ module.artifact ]
}

module "gcs_datos" {
  source           = "./modules/chatbot/gcs"
  bucket_name      = "rag-chroma-datos-${var.project_id}"
  region           = var.region
  modelos_llm_path = "${path.module}/../chatbot/gcs/chromadb_completa.xlsx"
}

module "chroma_vm" {
  source             = "./modules/chatbot/virtual_machine"
  project_id         = var.project_id
  region             = var.region
  zone               = var.zone
  vm_name            = "chroma-server"
  vm_machine_type    = "n2-standard-2"
  disk_size_gb       = 10
  vpc_network        = var.vpc_network
  subnet             = module.vpc_connector.subnet_id
  startup_script = templatefile("${path.module}/../chatbot/virtual_machine/inicio.sh.tpl", {
    project_id = var.project_id
  })
  depends_on = [module.vpc_connector, module.gcs_datos]
}

module "vpc_connector" {
  source       = "./modules/vpc"
  name         = "vpc-connector-chatbot"
  region       = var.region
  vpc_network  = var.vpc_network
  cidr_range   = "10.8.0.0/28"
  subnet_name  = var.subnet_name

  
}

# module "firestore" {
#   source      = "./modules/chatbot/firestore"
#   project_id  = var.project_id
#   name        = var.firestore_name
#   location_id = var.region
#   type        = "FIRESTORE_NATIVE"
# }

module "chatbot" {
  source                 = "./modules/chatbot/agente"
  project_id             = var.project_id
  region                 = var.region
  cloud_run_service_name = var.cloud_run_service_api_chatbot
  repository_name        = var.repository_name_api_chatbot
  image_name             = var.image_name_api_chatbot
  gemini_api_key         = var.gemini_api_key
  vpc_connector_id       = module.vpc_connector.connector_id

  depends_on             = [module.artifact]
}