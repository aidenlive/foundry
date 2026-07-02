variable "name" {
  description = "Base name; hyphens are stripped for the storage account."
  type        = string
}

variable "labels" {
  description = "Tags applied to the storage account."
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "Azure location."
  type        = string
}

variable "versioning" {
  description = "Enable blob versioning."
  type        = bool
  default     = true
}

variable "force_destroy" {
  description = "Accepted for contract parity; Azure deletes containers with blobs by default."
  type        = bool
  default     = false
}

variable "resource_group_name" {
  description = "Resource group for the storage account."
  type        = string
}

variable "container_name" {
  description = "Blob container to create."
  type        = string
  default     = "data"
}
