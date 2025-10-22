
# AWS Infrastructure for Mushroom Identifier
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# VPC
resource "aws_vpc" "mushroom_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "mushroom-vpc"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "mushroom_igw" {
  vpc_id = aws_vpc.mushroom_vpc.id

  tags = {
    Name = "mushroom-igw"
  }
}

# Public Subnets
resource "aws_subnet" "public_subnet" {
  count             = 2
  vpc_id            = aws_vpc.mushroom_vpc.id
  cidr_block        = "10.0.${count.index + 1}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]

  map_public_ip_on_launch = true

  tags = {
    Name = "mushroom-public-subnet-${count.index + 1}"
  }
}

# Security Group
resource "aws_security_group" "mushroom_sg" {
  name_prefix = "mushroom-"
  vpc_id      = aws_vpc.mushroom_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "mushroom-security-group"
  }
}

# Application Load Balancer
resource "aws_lb" "mushroom_alb" {
  name               = "mushroom-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.mushroom_sg.id]
  subnets            = aws_subnet.public_subnet[*].id

  tags = {
    Name = "mushroom-alb"
  }
}

# ECS Cluster
resource "aws_ecs_cluster" "mushroom_cluster" {
  name = "mushroom-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# ECS Task Definition
resource "aws_ecs_task_definition" "mushroom_task" {
  family                   = "mushroom-api"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = 512
  memory                   = 1024
  execution_role_arn       = aws_iam_role.ecs_execution_role.arn

  container_definitions = jsonencode([
    {
      name  = "mushroom-api"
      image = "mushroom-api:latest"
      portMappings = [
        {
          containerPort = 5000
          hostPort      = 5000
        }
      ]
      environment = [
        {
          name  = "FLASK_ENV"
          value = "production"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.mushroom_logs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

# ECS Service
resource "aws_ecs_service" "mushroom_service" {
  name            = "mushroom-service"
  cluster         = aws_ecs_cluster.mushroom_cluster.id
  task_definition = aws_ecs_task_definition.mushroom_task.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = aws_subnet.public_subnet[*].id
    security_groups  = [aws_security_group.mushroom_sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.mushroom_tg.arn
    container_name   = "mushroom-api"
    container_port   = 5000
  }
}

# CloudWatch Log Group
resource "aws_cloudwatch_log_group" "mushroom_logs" {
  name              = "/ecs/mushroom-api"
  retention_in_days = 30
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}
    