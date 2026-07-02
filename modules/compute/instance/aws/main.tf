data "aws_subnet" "target" {
  id = var.subnet_id
}

data "aws_ami" "ubuntu" {
  count       = var.image == "" ? 1 : 0
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

locals {
  ami_id = var.image != "" ? var.image : data.aws_ami.ubuntu[0].id
}

resource "aws_key_pair" "this" {
  count      = var.ssh_public_key != "" ? 1 : 0
  key_name   = var.name
  public_key = var.ssh_public_key
  tags       = var.labels
}

resource "aws_security_group" "this" {
  name        = var.name
  description = "Foundry-managed instance SG for ${var.name}: deny inbound by default"
  vpc_id      = data.aws_subnet.target.vpc_id
  tags        = merge(var.labels, { Name = var.name })
}

resource "aws_vpc_security_group_ingress_rule" "ssh" {
  count = length(var.allow_ssh_cidrs)

  security_group_id = aws_security_group.this.id
  cidr_ipv4         = var.allow_ssh_cidrs[count.index]
  from_port         = 22
  to_port           = 22
  ip_protocol       = "tcp"
  description       = "SSH (explicitly allowed by configuration)"
}

resource "aws_vpc_security_group_egress_rule" "all" {
  security_group_id = aws_security_group.this.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1"
  description       = "Allow all egress"
}

resource "aws_instance" "this" {
  ami                         = local.ami_id
  instance_type               = var.size
  subnet_id                   = var.subnet_id
  vpc_security_group_ids      = [aws_security_group.this.id]
  key_name                    = var.ssh_public_key != "" ? aws_key_pair.this[0].key_name : null
  associate_public_ip_address = var.public_ip
  user_data                   = var.user_data != "" ? var.user_data : null

  metadata_options {
    http_endpoint = "enabled"
    http_tokens   = "required" # IMDSv2 only
  }

  root_block_device {
    volume_size = var.root_volume_gb
    volume_type = "gp3"
    encrypted   = true
  }

  tags = merge(var.labels, { Name = var.name })
}
