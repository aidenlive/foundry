variable "name" {
  description = "Fully qualified zone name."
  type        = string
}

variable "labels" {
  description = "Tags applied to the zone."
  type        = map(string)
  default     = {}
}

variable "resource_group_name" {
  description = "Resource group for the zone."
  type        = string
}
