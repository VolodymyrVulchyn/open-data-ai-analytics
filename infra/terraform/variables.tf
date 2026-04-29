variable "resource_group_name" {
  description = "Name of the Azure Resource Group"
  type        = string
  default     = "rg-open-data-lab4"
}

variable "location" {
  description = "Azure region where resources will be created"
  type        = string
  default     = "westeurope"
}

variable "admin_username" {
  description = "Admin username for Linux VM"
  type        = string
  default     = "azureuser"
}

variable "vm_size" {
  description = "Size of Azure Linux VM"
  type        = string
  default     = "Standard_B1s"
}

variable "repo_url" {
  description = "GitHub repository URL with Docker project"
  type        = string
  default     = "https://github.com/VolodymyrVulchyn/open-data-ai-analytics.git"
}

variable "web_port" {
  description = "Port for web interface"
  type        = number
  default     = 8000
}