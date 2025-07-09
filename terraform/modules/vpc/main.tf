resource "google_compute_network" "rag_vpc" {
  name                    = var.vpc_network
  auto_create_subnetworks = false
  
}

resource "google_compute_firewall" "allow_fastapi" {
  name    = "allow-fastapi"
 network = google_compute_network.rag_vpc.name


  allow {
    protocol = "tcp"
    ports    = ["8080"]
  }

  direction     = "INGRESS"
  source_ranges = ["0.0.0.0/0"]

  target_tags = ["chroma"]

  description = "Permite tráfico HTTP a FastAPI en el puerto 8080 desde cualquier IP"
}
resource "google_compute_subnetwork" "rag_subnet" {
  name          = var.subnet_name
  ip_cidr_range = "10.10.0.0/24"
  region        = var.region
  network       = google_compute_network.rag_vpc.id
  
}

resource "google_vpc_access_connector" "connector" {
  name           = var.name
  region         = var.region
  network        = google_compute_network.rag_vpc.id
  ip_cidr_range  = var.cidr_range
  min_throughput = 200
  max_throughput = 300
}
