variable "foundry_context" {
  description = "Rendered Foundry configuration (injected by `foundry stack` via .foundry/stack.tfvars.json)."
  type        = any
}

variable "vpc_id" {
  description = "VPC UUID from the network stack (pass with -var, or wire terraform_remote_state in main.tf)."
  type        = string
  default     = null
}
