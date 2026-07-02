variable "name" {
  description = "Droplet name."
  type        = string
}

variable "labels" {
  description = "Converted to DO tags as key:value strings."
  type        = map(string)
  default     = {}
}

variable "size" {
  description = "Droplet size slug (e.g. s-1vcpu-1gb)."
  type        = string
}

variable "image" {
  description = "Image slug; defaults to Ubuntu 22.04 LTS."
  type        = string
  default     = "ubuntu-22-04-x64"
}

variable "subnet_id" {
  description = "DigitalOcean VPC UUID (DO has no subnets; the VPC is the boundary)."
  type        = string
}

variable "region" {
  description = "Region slug (e.g. nyc3)."
  type        = string
}

variable "ssh_public_key" {
  description = "OpenSSH public key; registered and attached when set."
  type        = string
  default     = ""
}

variable "allow_ssh_cidrs" {
  description = "CIDRs allowed to reach tcp/22 via a cloud firewall. Empty keeps SSH closed."
  type        = list(string)
  default     = []
}

variable "user_data" {
  description = "cloud-init user data."
  type        = string
  default     = ""
}

variable "public_ip" {
  description = "Droplets always receive a public IPv4; false only skips the output."
  type        = bool
  default     = false
}
