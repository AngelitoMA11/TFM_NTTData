output "chroma_vm_internal_ip" {
  description = "IP interna de la VM ChromaDB"
  value       = google_compute_instance.chroma_vm.network_interface[0].network_ip
}
