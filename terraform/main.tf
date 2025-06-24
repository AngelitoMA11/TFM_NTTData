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

module "function_limpieza" {
  source = "./modules/data/function_limpieza"
  project_id     = var.project_id
  region         = var.region
  name           = "limpieza"
  entry_point    = "procesar_csv"
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
}

module "injector" {
  source             = "./modules/data/url_injector"
  project_id         = var.project_id
  region             = var.region
  streamlit_name     = module.streamlit.streamlit_name
  function_limpieza  = module.function_limpieza.function_limpieza_url
  depends_on         = [module.streamlit, module.function_limpieza]
}
