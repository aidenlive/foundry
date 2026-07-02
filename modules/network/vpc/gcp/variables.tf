variable "name" {
  description = "Base name for the network and child resources."
  type        = string
}

variable "labels" {
  description = "Labels applied where GCP supports them."
  type        = map(string)
  default     = {}
}

variable "cidr" {
  description = "Overall environment CIDR (informational on GCP; subnets carry the ranges)."
  type        = string
}

variable "region" {
  description = "GCP region for subnetworks and Cloud NAT."
  type        = string
}

variable "public_subnets" {
  description = "CIDRs for subnetworks whose instances may attach external IPs."
  type        = list(string)
  default     = []
}

variable "private_subnets" {
  description = "CIDRs for subnetworks with Private Google Access and no external IPs."
  type        = list(string)
  default     = []
}

variable "enable_nat" {
  description = "Create Cloud Router + Cloud NAT for private egress."
  type        = bool
  default     = false
}
