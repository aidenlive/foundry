variable "name" {
  description = "Instance name."
  type        = string
}

variable "labels" {
  description = "Labels applied to the instance (values are lowercased by GCP conventions)."
  type        = map(string)
  default     = {}
}

variable "size" {
  description = "Machine type (e.g. e2-small)."
  type        = string
}

variable "image" {
  description = "Boot image; defaults to Ubuntu 22.04 LTS."
  type        = string
  default     = "ubuntu-os-cloud/ubuntu-2204-lts"
}

variable "subnet_id" {
  description = "Subnetwork self link or ID."
  type        = string
}

variable "region" {
  description = "Region used to derive the default zone."
  type        = string
}

variable "zone" {
  description = "Zone; defaults to <region>-a."
  type        = string
  default     = ""
}

variable "ssh_public_key" {
  description = "OpenSSH public key; added as ubuntu user metadata when set."
  type        = string
  default     = ""
}

variable "allow_ssh_cidrs" {
  description = "Ignored here: on GCP, ingress is governed by network firewall rules (see network/vpc/gcp)."
  type        = list(string)
  default     = []
}

variable "user_data" {
  description = "cloud-init user data (startup metadata)."
  type        = string
  default     = ""
}

variable "public_ip" {
  description = "Attach an ephemeral external IP."
  type        = bool
  default     = false
}

variable "root_volume_gb" {
  description = "Boot disk size in GB."
  type        = number
  default     = 20
}
