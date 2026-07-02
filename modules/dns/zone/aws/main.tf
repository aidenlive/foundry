resource "aws_route53_zone" "this" {
  name = var.name
  tags = var.labels
}
