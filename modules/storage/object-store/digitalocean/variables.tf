variable "name" {
  description = "Spaces bucket name (unique per region)."
  type        = string
}

variable "labels" {
  description = "Accepted for contract parity; Spaces buckets do not support tags."
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "Spaces region slug (e.g. nyc3)."
  type        = string
}

variable "versioning" {
  description = "Enable object versioning."
  type        = bool
  default     = true
}

variable "force_destroy" {
  description = "Allow destroying a non-empty bucket."
  type        = bool
  default     = false
}
