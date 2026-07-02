variable "name" {
  description = "Bucket name (globally unique)."
  type        = string
}

variable "labels" {
  description = "Labels applied to the bucket."
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "Bucket location (region or multi-region)."
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
