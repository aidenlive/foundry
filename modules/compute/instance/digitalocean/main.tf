locals {
  tag_list = [for k, v in var.labels : "${k}:${v}"]
}

resource "digitalocean_ssh_key" "this" {
  count      = var.ssh_public_key != "" ? 1 : 0
  name       = var.name
  public_key = var.ssh_public_key
}

resource "digitalocean_droplet" "this" {
  name       = var.name
  region     = var.region
  size       = var.size
  image      = var.image
  vpc_uuid   = var.subnet_id
  ssh_keys   = var.ssh_public_key != "" ? [digitalocean_ssh_key.this[0].fingerprint] : []
  user_data  = var.user_data != "" ? var.user_data : null
  tags       = local.tag_list
  monitoring = true
  backups    = false
}

resource "digitalocean_firewall" "this" {
  name        = "${var.name}-fw"
  droplet_ids = [digitalocean_droplet.this.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = length(var.allow_ssh_cidrs) > 0 ? var.allow_ssh_cidrs : ["127.0.0.1/32"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
