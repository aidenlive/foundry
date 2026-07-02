variable "name" {
  description = "Bucket name (globally unique)."
  type        = string
}

variable "labels" {
  description = "Tags applied to the bucket."
  type        = map(string)
  default     = {}
}

variable "region" {
  description = "AWS region (informational; provider config wins)."
  type        = string
  default     = ""
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
