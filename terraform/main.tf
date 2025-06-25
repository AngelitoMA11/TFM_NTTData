terraform {
  backend "gcs" {
    bucket  = "tfm-bucket-nttdata"
    prefix  = "estado" 
  }
}
# module "gitaction" {
#   source              = "./modules/gitaction"
#   project_id          = var.project_id
#   region                 = var.region
#   wif_pool_name       = "github-pool"
#   wif_provider_id     = "github-provider"
#   github_repo         = "AngelitoMA11/TFM_NTTData"
#   service_account_id  = "gcp-deploy"
#   service_account_role = "roles/editor"
# }

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
  repo_names  = [var.repository_name_api_streamlit, var.repository_name_grafana]
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

  depends_on             = [module.artifact]
}

module "injector" {
  source             = "./modules/data/url_injector"
  project_id         = var.project_id
  region             = var.region
  streamlit_name     = module.streamlit.streamlit_name
  function_limpieza  = module.function_limpieza.function_limpieza_url
  depends_on         = [module.streamlit, module.function_limpieza]
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