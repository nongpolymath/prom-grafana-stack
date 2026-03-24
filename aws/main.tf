provider "aws" {
  region = "us-east-1"
}

variable "instance_type" {
  default = "t2.medium"
}

# NOTE: Replace with a valid Key Pair name from your AWS account
variable "key_name" {
  default = "my-aws-key" 
}

resource "aws_security_group" "monitoring_stack_sg" {
  name        = "monitoring-stack-sg"
  description = "Allow inbound traffic for Monitoring Stack"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
    description = "SSH"
  }

  # Application Ports (Grafana, Prometheus, App, Alertmanager)
  # In production, restrict cidr_blocks to your IP or VPN
  dynamic "port" {
    for_each = [3000, 9090, 5000, 9093]
    content {
      from_port   = port.value
      to_port     = port.value
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "app_server" {
  ami           = "ami-0c7217cdde317cfec" # Example Ubuntu 22.04 LTS (US-East-1). UPDATE THIS.
  instance_type = var.instance_type
  key_name      = var.key_name
  vpc_security_group_ids = [aws_security_group.monitoring_stack_sg.id]

  tags = {
    Name = "Prometheus-Grafana-Stack"
  }
}

output "public_ip" {
  value = aws_instance.app_server.public_ip
}