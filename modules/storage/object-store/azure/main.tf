locals {
  account_name = substr(replace(lower(var.name), "-", ""), 0, 24)
}

resource "azurerm_storage_account" "this" {
  name                     = local.account_name
  resource_group_name      = var.resource_group_name
  location                 = var.region
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  tags                     = var.labels

  allow_nested_items_to_be_public = false

  blob_properties {
    versioning_enabled = var.versioning
  }
}

resource "azurerm_storage_container" "this" {
  name                  = var.container_name
  storage_account_id    = azurerm_storage_account.this.id
  container_access_type = "private"
}
