variable "name" {
  description = "Base name for the VPC and child resources."
  type        = string
}

variable "labels" {
  description = "Tags applied to every resource."
  type        = map(string)
  default     = {}
}

variable "cidr" {
  description = "IPv4 CIDR block for the VPC."
  type        = string
}

variable "region" {
  description = "AWS region (informational; provider config wins)."
  type        = string
  default     = ""
}

variable "public_subnets" {
  description = "CIDRs for public subnets, one per AZ in order."
  type        = list(string)
  default     = []
}

variable "private_subnets" {
  description = "CIDRs for private subnets, one per AZ in order."
  type        = list(string)
  default     = []
}

variable "enable_nat" {
  description = "Create a single NAT gateway for private subnet egress."
  type        = bool
  default     = false
}
