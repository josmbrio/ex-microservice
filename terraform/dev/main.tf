provider "aws" {
  region = "us-east-1"
}

variable vpc_cidr_block {}
variable subnet_cidr_block_a {}
variable subnet_cidr_block_b {}
variable env_prefix {}
variable avail_zone_a {}
variable avail_zone_b {}
variable source_ip {}
variable instance_type {}
variable public_key_location {}
variable app_port {}

resource "aws_vpc" "ex-microserice-vpc" {
  cidr_block = var.vpc_cidr_block
  tags = {
    Name: "${var.env_prefix}-vpc"
  }
}

resource "aws_subnet" "ex-microserice-subnet-a" {
  vpc_id = aws_vpc.ex-microserice-vpc.id
  cidr_block = var.subnet_cidr_block_a
  availability_zone = var.avail_zone_a
  tags = {
    Name: "${var.env_prefix}-subnet"
  }
}

resource "aws_subnet" "ex-microserice-subnet-b" {
  vpc_id = aws_vpc.ex-microserice-vpc.id
  cidr_block = var.subnet_cidr_block_b
  availability_zone = var.avail_zone_b
  tags = {
    Name: "${var.env_prefix}-subnet"
  }
}

resource "aws_internet_gateway" "ex-microserice-igw" {
  vpc_id = aws_vpc.ex-microserice-vpc.id
  tags = {
    Name = "${var.env_prefix}-igw"
  }
}

resource "aws_default_route_table" "main-rtb" {
  default_route_table_id = aws_vpc.ex-microserice-vpc.default_route_table_id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.ex-microserice-igw.id
  }
  tags = {
    Name = "${var.env_prefix}-main-rtb"
  }
}

resource "aws_default_security_group" "default-sg" {
  vpc_id = aws_vpc.ex-microserice-vpc.id
  ingress {
    from_port = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = [var.source_ip]
  }
  ingress {
    from_port = 80
    to_port = 80
    protocol = "tcp"
    cidr_blocks = [var.source_ip]
  }
  ingress {
    from_port = 443
    to_port = 443
    protocol = "tcp"
    cidr_blocks = [var.source_ip]
  }
  ingress {
    from_port = var.app_port
    to_port = var.app_port
    protocol = "tcp"
    cidr_blocks = [var.source_ip]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    prefix_list_ids = []
  }
  tags = {
    Name = "${var.env_prefix}-sg"
  }
}

data "aws_ami" "latest-amazon-linux-image" {
  most_recent = true
  owners = ["amazon"]
  filter {
    name = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
  filter {
    name = "virtualization-type"
    values = ["hvm"]
  }
}

output "aws_ami" {
  value = data.aws_ami.latest-amazon-linux-image.id
}

resource "aws_key_pair" "ssh-key" {
  key_name = "server-key-access"
  public_key = file(var.public_key_location)
}

resource "aws_instance" "ex-microserice-server-1" {
  ami = data.aws_ami.latest-amazon-linux-image.id
  instance_type = var.instance_type
  subnet_id = aws_subnet.ex-microserice-subnet-a.id
  vpc_security_group_ids = [aws_default_security_group.default-sg.id]
  availability_zone = var.avail_zone_a
  associate_public_ip_address = true
  key_name = aws_key_pair.ssh-key.key_name
  user_data = file("entry-script.sh")
  tags = {
    Name = "${var.env_prefix}-server"
  }
}

resource "aws_instance" "ex-microserice-server-2" {
  ami = data.aws_ami.latest-amazon-linux-image.id
  instance_type = var.instance_type
  subnet_id = aws_subnet.ex-microserice-subnet-b.id
  vpc_security_group_ids = [aws_default_security_group.default-sg.id]
  availability_zone = var.avail_zone_b
  associate_public_ip_address = true
  key_name = aws_key_pair.ssh-key.key_name
  user_data = file("entry-script.sh")
  tags = {
    Name = "${var.env_prefix}-server"
  }
}

output "ec2_public_ip_server_1" {
  value = aws_instance.ex-microserice-server-1.public_ip
}

output "ec2_public_ip_server_2" {
  value = aws_instance.ex-microserice-server-2.public_ip
}

resource "aws_lb" "ex_micro_lb" {
  name               = "ex-micro-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_default_security_group.default-sg.id]
  subnets            = [aws_subnet.ex-microserice-subnet-a.id, aws_subnet.ex-microserice-subnet-b.id]

  enable_deletion_protection = false

  tags = {
    Environment = "dev"
  }
}

resource "aws_lb_target_group" "ex_micro_tg" {
  name     = "ex-micro-lb"
  port     = 9000
  protocol = "HTTP"
  vpc_id   = aws_vpc.ex-microserice-vpc.id
}

resource "aws_lb_target_group_attachment" "ex_micro_tga1" {
  target_group_arn = aws_lb_target_group.ex_micro_tg.arn
  target_id        = aws_instance.ex-microserice-server-1.id
  port             = 9000
}

resource "aws_lb_target_group_attachment" "ex_micro_tga2" {
  target_group_arn = aws_lb_target_group.ex_micro_tg.arn
  target_id        = aws_instance.ex-microserice-server-2.id
  port             = 9000
}

resource "aws_lb_listener" "ex-micro-listener" {
  load_balancer_arn = aws_lb.ex_micro_lb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ex_micro_tg.arn
  }
}



