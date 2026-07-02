output "bucket_id" {
  description = "Container identifier."
  value       = azurerm_storage_container.this.id
}

output "bucket_name" {
  description = "Container name."
  value       = azurerm_storage_container.this.name
}

output "storage_account_name" {
  description = "Underlying storage account name."
  value       = azurerm_storage_account.this.name
}
