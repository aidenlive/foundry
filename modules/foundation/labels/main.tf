locals {
  delimiter = var.delimiter
  parts     = [var.org, var.project, var.environment]
  prefix    = join(local.delimiter, compact(local.parts))

  base_labels = {
    "managed-by"  = "foundry"
    "org"         = var.org
    "project"     = var.project
    "environment" = var.environment
  }

  labels = merge(local.base_labels, var.extra_labels)
}
