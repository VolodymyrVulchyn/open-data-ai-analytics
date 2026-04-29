output "public_ip_address" {
  description = "Public IP address of the Azure VM"
  value       = azurerm_public_ip.main.ip_address
}

output "web_url" {
  description = "URL of the deployed web interface"
  value       = "http://${azurerm_public_ip.main.ip_address}:${var.web_port}"
}

output "ssh_command" {
  description = "SSH command to connect to the VM"
  value       = "ssh -i lab4_vm_key.pem ${var.admin_username}@${azurerm_public_ip.main.ip_address}"
}