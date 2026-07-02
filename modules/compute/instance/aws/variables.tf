variable "name" {
  description = "Instance name."
  type        = string
}

variable "labels" {
  description = "Tags applied to the instance and security group."
  type        = map(string)
  default     = {}
}

variable "size" {
  description = "EC2 instance type (e.g. t3.small)."
  type        = string
}

variable "image" {
  description = "AMI ID; defaults to the latest Ubuntu 22.04 LTS for the region."
  type        = string
  default     = ""
}

variable "subnet_id" {
  description = "Subnet to launch into."
  type        = string
}

variable "region" {
  description = "AWS region (informational; provider config wins)."
  type        = string
  default     = ""
}

variable "ssh_public_key" {
  description = "OpenSSH public key material; a key pair is created when set."
  type        = string
  default     = ""
}

variable "allow_ssh_cidrs" {
  description = "CIDRs allowed to reach tcp/22. Empty (default) keeps SSH closed."
  type        = list(string)
  default     = []
}

variable "user_data" {
  description = "cloud-init user data."
  type        = string
  default     = ""
}

variable "public_ip" {
  description = "Associate a public IP address."
  type        = bool
  default     = false
}

variable "root_volume_gb" {
  description = "Root EBS volume size in GiB."
  type        = number
  default     = 20
}
