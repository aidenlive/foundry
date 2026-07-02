locals {
  image_parts = split(":", var.image)
}

resource "azurerm_public_ip" "this" {
  count = var.public_ip ? 1 : 0

  name                = "${var.name}-ip"
  location            = var.region
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard"
  tags                = var.labels
}

resource "azurerm_network_security_group" "this" {
  name                = "${var.name}-nsg"
  location            = var.region
  resource_group_name = var.resource_group_name
  tags                = var.labels
}

resource "azurerm_network_security_rule" "ssh" {
  count = length(var.allow_ssh_cidrs) > 0 ? 1 : 0

  name                        = "allow-ssh"
  priority                    = 1000
  direction                   = "Inbound"
  access                      = "Allow"
  protocol                    = "Tcp"
  source_port_range           = "*"
  destination_port_range      = "22"
  source_address_prefixes     = var.allow_ssh_cidrs
  destination_address_prefix  = "*"
  resource_group_name         = var.resource_group_name
  network_security_group_name = azurerm_network_security_group.this.name
}

resource "azurerm_network_interface" "this" {
  name                = "${var.name}-nic"
  location            = var.region
  resource_group_name = var.resource_group_name
  tags                = var.labels

  ip_configuration {
    name                          = "primary"
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = var.public_ip ? azurerm_public_ip.this[0].id : null
  }
}

resource "azurerm_network_interface_security_group_association" "this" {
  network_interface_id      = azurerm_network_interface.this.id
  network_security_group_id = azurerm_network_security_group.this.id
}

resource "azurerm_linux_virtual_machine" "this" {
  name                            = var.name
  location                        = var.region
  resource_group_name             = var.resource_group_name
  size                            = var.size
  admin_username                  = var.admin_username
  disable_password_authentication = true
  network_interface_ids           = [azurerm_network_interface.this.id]
  custom_data                     = var.user_data != "" ? base64encode(var.user_data) : null
  tags                            = var.labels

  admin_ssh_key {
    username   = var.admin_username
    public_key = var.ssh_public_key
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
    disk_size_gb         = var.root_volume_gb
  }

  source_image_reference {
    publisher = local.image_parts[0]
    offer     = local.image_parts[1]
    sku       = local.image_parts[2]
    version   = local.image_parts[3]
  }
}
