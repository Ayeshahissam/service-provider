# DevOps Assignment - Command Summary
# All commands used during the Kubernetes deployment process

Write-Host "=== DevOps Assignment Command Summary ===" -ForegroundColor Green
Write-Host "Service Provider Web Application - Kubernetes Deployment" -ForegroundColor Yellow
Write-Host ""

# ============================================================================
# PHASE 1: ENVIRONMENT SETUP
# ============================================================================
Write-Host "PHASE 1: ENVIRONMENT SETUP" -ForegroundColor Cyan
Write-Host "Commands to prepare the minikube environment:" -ForegroundColor White

Write-Host ""
Write-Host "# Start minikube cluster" -ForegroundColor Gray
Write-Host "minikube start" -ForegroundColor Green

Write-Host ""
Write-Host "# Enable required addons for HPA and ingress" -ForegroundColor Gray
Write-Host "minikube addons enable metrics-server" -ForegroundColor Green
Write-Host "minikube addons enable ingress" -ForegroundColor Green

Write-Host ""
Write-Host "# Verify minikube is running" -ForegroundColor Gray
Write-Host "minikube status" -ForegroundColor Green

# ============================================================================
# PHASE 2: DOCKER IMAGE PREPARATION
# ============================================================================
Write-Host ""
Write-Host "PHASE 2: DOCKER IMAGE PREPARATION" -ForegroundColor Cyan
Write-Host "Commands to build and load the application image:" -ForegroundColor White

Write-Host ""
Write-Host "# Build the web application Docker image" -ForegroundColor Gray
Write-Host "docker build -t service-provider-web:latest ." -ForegroundColor Green

Write-Host ""
Write-Host "# Load the image into minikube's Docker daemon" -ForegroundColor Gray
Write-Host "minikube image load service-provider-web:latest" -ForegroundColor Green

Write-Host ""
Write-Host "# Verify the image is loaded in minikube" -ForegroundColor Gray
Write-Host "minikube image ls | findstr service-provider" -ForegroundColor Green

# ============================================================================
# PHASE 3: KUBERNETES DEPLOYMENT
# ============================================================================
Write-Host ""
Write-Host "PHASE 3: KUBERNETES DEPLOYMENT" -ForegroundColor Cyan
Write-Host "Commands to deploy all components to Kubernetes:" -ForegroundColor White

Write-Host ""
Write-Host "# Deploy all components at once" -ForegroundColor Gray
Write-Host "kubectl apply -f k8s-deploy-all.yaml" -ForegroundColor Green

Write-Host ""
Write-Host "# Alternative: Deploy components individually" -ForegroundColor Gray
Write-Host "kubectl apply -f k8s-mongodb-pvc.yaml" -ForegroundColor Yellow
Write-Host "kubectl apply -f k8s-mongodb-deployment.yaml" -ForegroundColor Yellow
Write-Host "kubectl apply -f k8s-mongodb-service.yaml" -ForegroundColor Yellow
Write-Host "kubectl apply -f k8s-webapp-deployment.yaml" -ForegroundColor Yellow
Write-Host "kubectl apply -f k8s-webapp-service.yaml" -ForegroundColor Yellow
Write-Host "kubectl apply -f k8s-webapp-hpa.yaml" -ForegroundColor Yellow

# ============================================================================
# PHASE 4: VERIFICATION AND MONITORING
# ============================================================================
Write-Host ""
Write-Host "PHASE 4: VERIFICATION AND MONITORING" -ForegroundColor Cyan
Write-Host "Commands to verify and monitor the deployment:" -ForegroundColor White

Write-Host ""
Write-Host "# Check all pods status" -ForegroundColor Gray
Write-Host "kubectl get pods" -ForegroundColor Green

Write-Host ""
Write-Host "# Check all services" -ForegroundColor Gray
Write-Host "kubectl get services" -ForegroundColor Green

Write-Host ""
Write-Host "# Check persistent volume claims" -ForegroundColor Gray
Write-Host "kubectl get pvc" -ForegroundColor Green

Write-Host ""
Write-Host "# Check horizontal pod autoscaler" -ForegroundColor Gray
Write-Host "kubectl get hpa" -ForegroundColor Green

Write-Host ""
Write-Host "# Get detailed deployment information" -ForegroundColor Gray
Write-Host "kubectl get deployments -o wide" -ForegroundColor Green

# ============================================================================
# PHASE 5: TROUBLESHOOTING (PERFORMED DURING ASSIGNMENT)
# ============================================================================
Write-Host ""
Write-Host "PHASE 5: TROUBLESHOOTING (ImagePullBackOff Issue)" -ForegroundColor Cyan
Write-Host "Commands used to diagnose and fix the deployment issue:" -ForegroundColor White

Write-Host ""
Write-Host "# Describe problematic pod to see error details" -ForegroundColor Gray
Write-Host "kubectl describe pod webapp-deployment-6676c5ddc7-r4bgq" -ForegroundColor Red

Write-Host ""
Write-Host "# Check if image exists in minikube" -ForegroundColor Gray
Write-Host "minikube image ls | findstr service-provider" -ForegroundColor Red

Write-Host ""
Write-Host "# Fix: Updated deployment with imagePullPolicy: Never" -ForegroundColor Gray
Write-Host "kubectl apply -f k8s-webapp-deployment.yaml" -ForegroundColor Green

Write-Host ""
Write-Host "# Verify fix worked" -ForegroundColor Gray
Write-Host "kubectl get pods" -ForegroundColor Green

# ============================================================================
# PHASE 6: APPLICATION ACCESS
# ============================================================================
Write-Host ""
Write-Host "PHASE 6: APPLICATION ACCESS" -ForegroundColor Cyan
Write-Host "Commands to access the deployed application:" -ForegroundColor White

Write-Host ""
Write-Host "# Get application URL (LoadBalancer service)" -ForegroundColor Gray
Write-Host "minikube service webapp-service --url" -ForegroundColor Green

Write-Host ""
Write-Host "# Alternative: Port forwarding method" -ForegroundColor Gray
Write-Host "kubectl port-forward service/webapp-service 8080:80" -ForegroundColor Yellow

# ============================================================================
# PHASE 7: MONITORING AND TESTING
# ============================================================================
Write-Host ""
Write-Host "PHASE 7: MONITORING AND TESTING" -ForegroundColor Cyan
Write-Host "Commands for monitoring and testing auto-scaling:" -ForegroundColor White

Write-Host ""
Write-Host "# Watch pods in real-time" -ForegroundColor Gray
Write-Host "kubectl get pods --watch" -ForegroundColor Green

Write-Host ""
Write-Host "# Watch HPA status" -ForegroundColor Gray
Write-Host "kubectl get hpa --watch" -ForegroundColor Green

Write-Host ""
Write-Host "# Check resource usage" -ForegroundColor Gray
Write-Host "kubectl top pods" -ForegroundColor Green
Write-Host "kubectl top nodes" -ForegroundColor Green

Write-Host ""
Write-Host "# View application logs" -ForegroundColor Gray
Write-Host "kubectl logs -l app=webapp" -ForegroundColor Green
Write-Host "kubectl logs -f deployment/webapp-deployment" -ForegroundColor Green

Write-Host ""
Write-Host "# Generate load for testing auto-scaling" -ForegroundColor Gray
Write-Host "kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh" -ForegroundColor Yellow

# ============================================================================
# PHASE 8: CLEANUP (OPTIONAL)
# ============================================================================
Write-Host ""
Write-Host "PHASE 8: CLEANUP (OPTIONAL)" -ForegroundColor Cyan
Write-Host "Commands to clean up the deployment:" -ForegroundColor White

Write-Host ""
Write-Host "# Delete all resources" -ForegroundColor Gray
Write-Host "kubectl delete -f k8s-deploy-all.yaml" -ForegroundColor Red

Write-Host ""
Write-Host "# Stop minikube" -ForegroundColor Gray
Write-Host "minikube stop" -ForegroundColor Red

# ============================================================================
# FINAL STATUS
# ============================================================================
Write-Host ""
Write-Host "=== FINAL DEPLOYMENT STATUS ===" -ForegroundColor Green
Write-Host "✅ MongoDB: 1 replica running with 5Gi persistent storage" -ForegroundColor White
Write-Host "✅ Web App: 3 replicas running (auto-scalable to 10)" -ForegroundColor White
Write-Host "✅ Services: LoadBalancer (web) + NodePort (database)" -ForegroundColor White
Write-Host "✅ Auto-scaling: HPA configured for CPU (70%) and Memory (80%)" -ForegroundColor White
Write-Host "✅ Health Checks: Liveness and readiness probes active" -ForegroundColor White
Write-Host "✅ Issue Resolution: ImagePullBackOff fixed with imagePullPolicy: Never" -ForegroundColor White

Write-Host ""
Write-Host "=== ASSIGNMENT REQUIREMENTS FULFILLED ===" -ForegroundColor Green
Write-Host "✅ Multiple replicas of web servers" -ForegroundColor White
Write-Host "✅ Single database server replica" -ForegroundColor White
Write-Host "✅ LoadBalancer service for web server" -ForegroundColor White
Write-Host "✅ NodePort service for database server" -ForegroundColor White
Write-Host "✅ Persistent Volume Claim for database" -ForegroundColor White
Write-Host "✅ HorizontalPodAutoscaler for auto-scaling" -ForegroundColor White
Write-Host "✅ Well-indented YAML files" -ForegroundColor White

Write-Host ""
Write-Host "Report generated on: $(Get-Date)" -ForegroundColor Yellow 