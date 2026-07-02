variable "name" {
  description = "Cluster name."
  type        = string
}

variable "labels" {
  description = "Tags applied to all resources."
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "AWS region (informational; provider config wins)."
  type        = string
  default     = ""
}

variable "version" {
  description = "Kubernetes version (e.g. 1.29); empty uses the EKS default."
  type        = string
  default     = ""
}

variable "node_size" {
  description = "EC2 instance type for the node group."
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
  description = "VPC ID (informational; subnets determine placement)."
  type        = string
  default     = ""
}

variable "subnet_ids" {
  description = "Subnets for the control plane and node group (2+ AZs recommended)."
  type        = list(string)
}
