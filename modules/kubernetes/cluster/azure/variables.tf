variable "name" {
  description = "Cluster name."
  type        = string
}

variable "labels" {
  description = "Tags applied to the cluster."
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "Azure location."
  type        = string
}

variable "version" {
  description = "Kubernetes version; empty uses the AKS default."
  type        = string
  default     = ""
}

variable "node_size" {
  description = "VM size for the default node pool."
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
  description = "VNet ID (informational; the subnet determines placement)."
  type        = string
  default     = ""
}

variable "subnet_ids" {
  description = "Exactly one subnet ID for the default node pool."
  type        = list(string)
}

variable "resource_group_name" {
  description = "Resource group for the cluster."
  type        = string
}
