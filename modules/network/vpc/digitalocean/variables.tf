variable "name" {
  description = "VPC name."
  type        = string
}

variable "labels" {
  description = "Accepted for contract compatibility; DO VPCs do not support tags."
  type        = map(string)
  default     = {}
}

variable "cidr" {
  description = "IP range for the VPC."
  type        = string
}

variable "region" {
  description = "DigitalOcean region slug (e.g. nyc3)."
  type        = string
}

variable "public_subnets" {
  description = "Ignored on DigitalOcean (no subnet primitive); kept for contract parity."
  type        = list(string)
  default     = []
}

variable "private_subnets" {
  description = "Ignored on DigitalOcean (no subnet primitive); kept for contract parity."
  type        = list(string)
  default     = []
}

variable "enable_nat" {
  description = "Ignored on DigitalOcean (egress is provided by the platform)."
  type        = bool
  default     = false
}
