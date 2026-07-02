variable "name" {
  description = "Virtual machine name."
  type        = string
}

variable "labels" {
  description = "Tags applied to every resource."
  type        = map(string)
  default     = {}
}

variable "size" {
  description = "VM size (e.g. Standard_B2s)."
  type        = string
}

variable "image" {
  description = "Image as publisher:offer:sku:version; defaults to Ubuntu 22.04 LTS."
  type        = string
  default     = "Canonical:0001-com-ubuntu-server-jammy:22_04-lts-gen2:latest"
}

variable "subnet_id" {
  description = "Subnet ID for the NIC."
  type        = string
}

variable "region" {
  description = "Azure location."
  type        = string
}

variable "resource_group_name" {
  description = "Resource group to create the VM in."
  type        = string
}

variable "admin_username" {
  description = "Admin user name."
  type        = string
  default     = "ubuntu"
}

variable "ssh_public_key" {
  description = "OpenSSH public key for the admin user (required: password auth is disabled)."
  type        = string
}

variable "allow_ssh_cidrs" {
  description = "CIDRs allowed to reach tcp/22 via a per-NIC NSG. Empty keeps SSH closed."
  type        = list(string)
  default     = []
}

variable "user_data" {
  description = "cloud-init user data."
  type        = string
  default     = ""
}

variable "public_ip" {
  description = "Attach a public IP address."
  type        = bool
  default     = false
}

variable "root_volume_gb" {
  description = "OS disk size in GB."
  type        = number
  default     = 30
}
