variable "name" {
  description = "Cluster name."
  type        = string
}

variable "labels" {
  description = "Resource labels applied to the cluster."
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "GCP region (regional cluster)."
  type        = string
}

variable "version" {
  description = "Kubernetes version prefix; empty follows the REGULAR release channel."
  type        = string
  default     = ""
}

variable "node_size" {
  description = "Machine type for the system node pool."
  type        = string
}

variable "min_nodes" {
  description = "Minimum node count per zone."
  type        = number
  default     = 1
}

variable "max_nodes" {
  description = "Maximum node count per zone."
  type        = number
  default     = 3
}

variable "vpc_id" {
  description = "Network self link or ID."
  type        = string
}

variable "subnet_ids" {
  description = "Exactly one subnetwork self link/ID for the cluster."
  type        = list(string)
  default     = []
}

variable "project_id" {
  description = "GCP project ID (required for Workload Identity pool naming)."
  type        = string
}
