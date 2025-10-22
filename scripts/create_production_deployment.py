#!/usr/bin/env python3
"""
Create Production Deployment for Mushroom Identifier

This script creates production-ready deployment configurations and guides.
"""

from pathlib import Path

def create_docker_compose():
    """Create Docker Compose for production."""
    docker_compose = '''
version: '3.8'

services:
  mushroom-api:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - MODEL_PATH=/app/models
    volumes:
      - ./models:/app/models
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - mushroom-api
    restart: unless-stopped

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    restart: unless-stopped

  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB=mushroom_db
      - POSTGRES_USER=mushroom_user
      - POSTGRES_PASSWORD=mushroom_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
    '''
    
    compose_file = Path("docker-compose.yml")
    with open(compose_file, 'w') as f:
        f.write(docker_compose)
    
    print(f"🐳 Docker Compose created: {compose_file}")

def create_nginx_config():
    """Create Nginx configuration."""
    nginx_config = '''
events {
    worker_connections 1024;
}

http {
    upstream mushroom_api {
        server mushroom-api:5000;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    server {
        listen 80;
        server_name your-domain.com;

        # Redirect HTTP to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
        ssl_prefer_server_ciphers off;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # API endpoints
        location /api/ {
            limit_req zone=api burst=20 nodelay;
            
            proxy_pass http://mushroom_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            
            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }

        # Health check
        location /health {
            proxy_pass http://mushroom_api/health;
        }

        # Static files
        location /static/ {
            alias /app/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
    '''
    
    nginx_file = Path("nginx.conf")
    with open(nginx_file, 'w') as f:
        f.write(nginx_config)
    
    print(f"🌐 Nginx config created: {nginx_file}")

def create_kubernetes_manifests():
    """Create Kubernetes deployment manifests."""
    k8s_deployment = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mushroom-api
  labels:
    app: mushroom-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mushroom-api
  template:
    metadata:
      labels:
        app: mushroom-api
    spec:
      containers:
      - name: mushroom-api
        image: mushroom-api:latest
        ports:
        - containerPort: 5000
        env:
        - name: FLASK_ENV
          value: "production"
        - name: MODEL_PATH
          value: "/app/models"
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 5000
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: model-storage
          mountPath: /app/models
      volumes:
      - name: model-storage
        persistentVolumeClaim:
          claimName: model-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: mushroom-api-service
spec:
  selector:
    app: mushroom-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 5000
  type: LoadBalancer
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: model-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
    '''
    
    k8s_file = Path("k8s-deployment.yaml")
    with open(k8s_file, 'w') as f:
        f.write(k8s_deployment)
    
    print(f"☸️ Kubernetes manifest created: {k8s_file}")

def create_terraform_config():
    """Create Terraform configuration for cloud deployment."""
    terraform_main = '''
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
    '''
    
    terraform_file = Path("terraform/main.tf")
    terraform_file.parent.mkdir(exist_ok=True)
    
    with open(terraform_file, 'w') as f:
        f.write(terraform_main)
    
    print(f"🏗️ Terraform config created: {terraform_file}")

def create_ci_cd_pipeline():
    """Create CI/CD pipeline configuration."""
    github_actions = '''
name: Deploy Mushroom Identifier

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v --cov=src
    
    - name: Run linting
      run: |
        flake8 src/ tests/
        black --check src/ tests/
    
    - name: Security scan
      run: |
        bandit -r src/

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          mushroom-identifier:latest
          mushroom-identifier:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-west-2
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service \
          --cluster mushroom-cluster \
          --service mushroom-service \
          --force-new-deployment
    '''
    
    github_file = Path(".github/workflows/deploy.yml")
    github_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(github_file, 'w') as f:
        f.write(github_actions)
    
    print(f"🚀 GitHub Actions workflow created: {github_file}")

def create_monitoring_config():
    """Create monitoring and observability configuration."""
    prometheus_config = '''
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'mushroom-api'
    static_configs:
      - targets: ['mushroom-api:5000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'nginx'
    static_configs:
      - targets: ['nginx:9113']
    '''
    
    prometheus_file = Path("monitoring/prometheus.yml")
    prometheus_file.parent.mkdir(exist_ok=True)
    
    with open(prometheus_file, 'w') as f:
        f.write(prometheus_config)
    
    print(f"📊 Prometheus config created: {prometheus_file}")

def create_production_guide():
    """Create comprehensive production deployment guide."""
    guide = '''
# 🚀 Production Deployment Guide

## Overview
This guide covers deploying the Mushroom Identifier to production with high availability, security, and monitoring.

## Architecture Options

### 1. Docker Compose (Single Server)
```bash
# Deploy locally or on single server
docker-compose up -d
```

### 2. Kubernetes (Multi-Node)
```bash
# Deploy to Kubernetes cluster
kubectl apply -f k8s-deployment.yaml
```

### 3. AWS ECS (Managed Containers)
```bash
# Deploy to AWS ECS
terraform init
terraform plan
terraform apply
```

## Security Considerations

### 1. SSL/TLS
- Use Let's Encrypt for free SSL certificates
- Configure HTTPS redirects
- Implement HSTS headers

### 2. Authentication
- Add API key authentication
- Implement rate limiting
- Use JWT tokens for mobile apps

### 3. Data Protection
- Encrypt data at rest
- Use secure database connections
- Implement backup strategies

## Monitoring & Observability

### 1. Application Metrics
- Response times
- Error rates
- Request volumes
- Model accuracy

### 2. Infrastructure Metrics
- CPU/Memory usage
- Disk I/O
- Network traffic
- Database performance

### 3. Logging
- Structured logging with JSON
- Log aggregation (ELK stack)
- Error tracking (Sentry)

## Scaling Strategies

### 1. Horizontal Scaling
- Load balancers
- Auto-scaling groups
- Container orchestration

### 2. Database Scaling
- Read replicas
- Connection pooling
- Caching (Redis)

### 3. CDN
- Static asset delivery
- Global content distribution
- Edge caching

## Deployment Environments

### Development
- Local Docker containers
- Hot reloading
- Debug logging

### Staging
- Production-like environment
- Integration testing
- Performance testing

### Production
- High availability
- Monitoring
- Backup strategies

## Cost Optimization

### 1. Resource Sizing
- Right-size instances
- Use spot instances for non-critical workloads
- Implement auto-scaling

### 2. Storage
- Use appropriate storage classes
- Implement lifecycle policies
- Compress data

### 3. Network
- Use CDN for static content
- Optimize API responses
- Implement caching

## Disaster Recovery

### 1. Backup Strategy
- Automated database backups
- Model versioning
- Configuration backups

### 2. Recovery Procedures
- RTO: 1 hour
- RPO: 15 minutes
- Multi-region deployment

### 3. Testing
- Regular disaster recovery drills
- Backup restoration testing
- Failover procedures

## Performance Optimization

### 1. Application
- Code profiling
- Database query optimization
- Caching strategies

### 2. Infrastructure
- CDN implementation
- Load balancing
- Auto-scaling

### 3. Monitoring
- Performance baselines
- Alert thresholds
- Capacity planning

## Compliance & Governance

### 1. Data Privacy
- GDPR compliance
- Data retention policies
- User consent management

### 2. Security
- Vulnerability scanning
- Penetration testing
- Security audits

### 3. Documentation
- API documentation
- Runbooks
- Incident response procedures
    '''
    
    guide_file = Path("PRODUCTION_DEPLOYMENT.md")
    with open(guide_file, 'w') as f:
        f.write(guide)
    
    print(f"📖 Production guide created: {guide_file}")

def main():
    """Create production deployment components."""
    print("🚀 CREATING PRODUCTION DEPLOYMENT")
    print("=" * 50)
    
    # Create deployment configurations
    create_docker_compose()
    create_nginx_config()
    create_kubernetes_manifests()
    create_terraform_config()
    create_ci_cd_pipeline()
    create_monitoring_config()
    create_production_guide()
    
    print("\n🎉 Production Deployment Created!")
    print("=" * 40)
    print("📁 Files created:")
    print("   - docker-compose.yml (Container orchestration)")
    print("   - nginx.conf (Load balancer config)")
    print("   - k8s-deployment.yaml (Kubernetes manifests)")
    print("   - terraform/main.tf (AWS infrastructure)")
    print("   - .github/workflows/deploy.yml (CI/CD pipeline)")
    print("   - monitoring/prometheus.yml (Metrics config)")
    print("   - PRODUCTION_DEPLOYMENT.md (Deployment guide)")
    
    print("\n🚀 Deployment Options:")
    print("1. Docker Compose: docker-compose up -d")
    print("2. Kubernetes: kubectl apply -f k8s-deployment.yaml")
    print("3. AWS ECS: terraform apply")
    print("4. CI/CD: Push to main branch for auto-deployment")

if __name__ == "__main__":
    main()
