variable "name" {
  description = "Fully qualified zone name (without trailing dot)."
  type        = string
}

variable "labels" {
  description = "Labels applied to the zone."
  type        = map(string)
  default     = {}
}
