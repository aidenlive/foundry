variable "name" {
  description = "Base name for the VNet and child resources."
  type        = string
}

variable "labels" {
  description = "Tags applied to every resource."
  type        = map(string)
  default     = {}
}

variable "cidr" {
  description = "Address space for the virtual network."
  type        = string
}

variable "region" {
  description = "Azure location (e.g. eastus)."
  type        = string
}

variable "public_subnets" {
  description = "CIDRs for public-facing subnets."
  type        = list(string)
  default     = []
}

variable "private_subnets" {
  description = "CIDRs for private subnets (default-deny NSG attached)."
  type        = list(string)
  default     = []
}

variable "enable_nat" {
  description = "Create a NAT gateway for private subnet egress."
  type        = bool
  default     = false
}

variable "create_resource_group" {
  description = "Create the resource group; set false to use an existing one."
  type        = bool
  default     = true
}

variable "resource_group_name" {
  description = "Resource group name; defaults to <name>-rg when created."
  type        = string
  default     = ""
}
