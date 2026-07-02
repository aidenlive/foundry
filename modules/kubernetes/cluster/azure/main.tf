resource "azurerm_kubernetes_cluster" "this" {
  name                = var.name
  location            = var.region
  resource_group_name = var.resource_group_name
  dns_prefix          = var.name
  kubernetes_version  = var.version != "" ? var.version : null
  tags                = var.labels

  default_node_pool {
    name                 = "system"
    vm_size              = var.node_size
    auto_scaling_enabled = true
    min_count            = var.min_nodes
    max_count            = var.max_nodes
    vnet_subnet_id       = var.subnet_ids[0]
    tags                 = var.labels
  }

  identity {
    type = "SystemAssigned"
  }

  network_profile {
    network_plugin = "azure"
    network_policy = "azure"
  }
}
