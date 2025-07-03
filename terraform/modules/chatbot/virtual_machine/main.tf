# Crear cuenta de servicio para Grafana
resource "google_service_account" "VM-storage" {
  account_id   = "vm-storage"
  display_name = "Leer los archivos de GCS en VM"
}

resource "google_project_iam_member" "vm_gcs_access" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  member  = "serviceAccount:${google_service_account.VM-storage.email}"
}

resource "google_compute_instance" "chroma_vm" {
  name         = var.vm_name
  machine_type = var.vm_machine_type
  zone         = var.zone
  project      = var.project_id

  service_account {
    email  = google_service_account.VM-storage.email
    scopes = ["cloud-platform"]
  }
  

  boot_disk {
    initialize_params {
      image = "ubuntu-2204-lts"
    }
  }

  attached_disk {
    source      = google_compute_disk.chroma_disk.id
    device_name = "chroma-data"
  }

  metadata = {
    startup-script = var.startup_script
  }

  network_interface {
    network    = var.vpc_network
    subnetwork = var.subnet
    access_config {}  
  }

  tags = ["chroma", "ssh-access"]
  
}

resource "google_compute_disk" "chroma_disk" {
  name  = "${var.vm_name}-disk"
  type  = "pd-ssd"
  zone  = var.zone
  size  = var.disk_size_gb
}

