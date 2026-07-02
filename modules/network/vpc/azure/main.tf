locals {
  rg_name = var.resource_group_name != "" ? var.resource_group_name : "${var.name}-rg"
}

resource "azurerm_resource_group" "this" {
  count = var.create_resource_group ? 1 : 0

  name     = local.rg_name
  location = var.region
  tags     = var.labels
}

locals {
  resource_group_name = var.create_resource_group ? azurerm_resource_group.this[0].name : local.rg_name
}

resource "azurerm_virtual_network" "this" {
  name                = var.name
  location            = var.region
  resource_group_name = local.resource_group_name
  address_space       = [var.cidr]
  tags                = var.labels
}

resource "azurerm_subnet" "public" {
  count = length(var.public_subnets)

  name                 = "${var.name}-public-${count.index}"
  resource_group_name  = local.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = [var.public_subnets[count.index]]
}

resource "azurerm_subnet" "private" {
  count = length(var.private_subnets)

  name                 = "${var.name}-private-${count.index}"
  resource_group_name  = local.resource_group_name
  virtual_network_name = azurerm_virtual_network.this.name
  address_prefixes     = [var.private_subnets[count.index]]
}

resource "azurerm_network_security_group" "private" {
  count = length(var.private_subnets) > 0 ? 1 : 0

  name                = "${var.name}-private-nsg"
  location            = var.region
  resource_group_name = local.resource_group_name
  tags                = var.labels

  security_rule {
    name                       = "deny-inbound-internet"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
  }
}

resource "azurerm_subnet_network_security_group_association" "private" {
  count = length(var.private_subnets)

  subnet_id                 = azurerm_subnet.private[count.index].id
  network_security_group_id = azurerm_network_security_group.private[0].id
}

resource "azurerm_public_ip" "nat" {
  count = var.enable_nat ? 1 : 0

  name                = "${var.name}-nat-ip"
  location            = var.region
  resource_group_name = local.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
  tags                = var.labels
}

resource "azurerm_nat_gateway" "this" {
  count = var.enable_nat ? 1 : 0

  name                = "${var.name}-nat"
  location            = var.region
  resource_group_name = local.resource_group_name
  sku_name            = "Standard"
  tags                = var.labels
}

resource "azurerm_nat_gateway_public_ip_association" "this" {
  count = var.enable_nat ? 1 : 0

  nat_gateway_id       = azurerm_nat_gateway.this[0].id
  public_ip_address_id = azurerm_public_ip.nat[0].id
}

resource "azurerm_subnet_nat_gateway_association" "private" {
  count = var.enable_nat ? length(var.private_subnets) : 0

  subnet_id      = azurerm_subnet.private[count.index].id
  nat_gateway_id = azurerm_nat_gateway.this[0].id
}
