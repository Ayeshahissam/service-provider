# PowerShell script to deploy Service Provider app to Minikube
# Author: DevOps Assignment
# Description: Automated deployment script for Windows

Write-Host "=== Service Provider Minikube Deployment Script ===" -ForegroundColor Green

# Check if minikube is running
Write-Host "Checking Minikube status..." -ForegroundColor Yellow
$minikubeStatus = minikube status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Starting Minikube..." -ForegroundColor Yellow
    minikube start
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to start Minikube. Please check your installation." -ForegroundColor Red
        exit 1
    }
}

# Enable required addons
Write-Host "Enabling Minikube addons..." -ForegroundColor Yellow
minikube addons enable metrics-server
minikube addons enable ingress

# Build Docker image
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t service-provider-web:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to build Docker image." -ForegroundColor Red
    exit 1
}

# Load image into minikube
Write-Host "Loading image into Minikube..." -ForegroundColor Yellow
minikube image load service-provider-web:latest

# Deploy to Kubernetes
Write-Host "Deploying to Kubernetes..." -ForegroundColor Yellow

# Deploy MongoDB first
Write-Host "Deploying MongoDB..." -ForegroundColor Cyan
kubectl apply -f k8s-mongodb-pvc.yaml
kubectl apply -f k8s-mongodb-deployment.yaml
kubectl apply -f k8s-mongodb-service.yaml

# Wait for MongoDB to be ready
Write-Host "Waiting for MongoDB to be ready..." -ForegroundColor Cyan
kubectl wait --for=condition=available --timeout=300s deployment/mongodb-deployment

# Deploy Web Application
Write-Host "Deploying Web Application..." -ForegroundColor Cyan
kubectl apply -f k8s-webapp-deployment.yaml
kubectl apply -f k8s-webapp-service.yaml
kubectl apply -f k8s-webapp-hpa.yaml

# Wait for web app to be ready
Write-Host "Waiting for Web Application to be ready..." -ForegroundColor Cyan
kubectl wait --for=condition=available --timeout=300s deployment/webapp-deployment

# Show deployment status
Write-Host "`n=== Deployment Status ===" -ForegroundColor Green
kubectl get pods
kubectl get services
kubectl get hpa

# Get application URL
Write-Host "`n=== Application Access ===" -ForegroundColor Green
Write-Host "Getting application URL..." -ForegroundColor Yellow
$appUrl = minikube service webapp-service --url
Write-Host "Application is accessible at: $appUrl" -ForegroundColor Green

Write-Host "`n=== Deployment Complete! ===" -ForegroundColor Green
Write-Host "You can now access your Service Provider application." -ForegroundColor White
Write-Host "Use 'kubectl get pods --watch' to monitor pod status." -ForegroundColor White
Write-Host "Use 'kubectl get hpa --watch' to monitor auto-scaling." -ForegroundColor White 