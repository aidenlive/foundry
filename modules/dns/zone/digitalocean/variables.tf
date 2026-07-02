variable "name" {
  description = "Fully qualified zone name."
  type        = string
}

variable "labels" {
  description = "Accepted for contract parity; DO domains do not support tags."
  type        = map(string)
  default     = {}
}
