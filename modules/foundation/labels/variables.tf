variable "org" {
  description = "Organization name (metadata.name of the Organization document)."
  type        = string
}

variable "project" {
  description = "Project name."
  type        = string
}

variable "environment" {
  description = "Environment name (dev, staging, prod, ...)."
  type        = string
}

variable "delimiter" {
  description = "Separator used when composing resource names."
  type        = string
  default     = "-"
}

variable "extra_labels" {
  description = "Additional labels merged over the Foundry base label set."
  type        = map(string)
  default     = {}
}
