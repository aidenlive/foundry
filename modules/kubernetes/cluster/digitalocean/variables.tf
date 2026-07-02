variable "name" {
  description = "Cluster name."
  type        = string
}

variable "labels" {
  description = "Converted to DO tags as key:value strings."
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "Region slug (e.g. nyc3)."
  type        = string
}

variable "version" {
  description = "DOKS version slug; empty resolves the latest supported version."
  type        = string
  default     = ""
}

variable "node_size" {
  description = "Droplet size slug for the node pool."
  type        = string
}

variable "min_nodes" {
  description = "Minimum node count."
  type        = number
  default     = 1
}

variable "max_nodes" {
  description = "Maximum node count."
  type        = number
  default     = 3
}

variable "vpc_id" {
  description = "DigitalOcean VPC UUID."
  type        = string
}

variable "subnet_ids" {
  description = "Unused on DigitalOcean; kept for contract parity."
  type        = list(string)
  default     = []
}

variable "ha_control_plane" {
  description = "Enable the highly-available control plane (recommended for production)."
  type        = bool
  default     = false
}
