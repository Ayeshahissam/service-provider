# Cleanup Script for Minikube Resources
# DevOps Assignment - Service Provider Application

Write-Host "=== Minikube Cleanup Script ===" -ForegroundColor Red
Write-Host "This will delete all deployed resources and stop minikube" -ForegroundColor Yellow
Write-Host ""

# Ask for confirmation
$confirmation = Read-Host "Are you sure you want to delete all resources? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "Cleanup cancelled." -ForegroundColor Green
    exit
}

Write-Host ""
Write-Host "Starting cleanup process..." -ForegroundColor Yellow

# ============================================================================
# STEP 1: DELETE KUBERNETES RESOURCES
# ============================================================================
Write-Host ""
Write-Host "STEP 1: Deleting Kubernetes Resources" -ForegroundColor Cyan

Write-Host "Deleting HorizontalPodAutoscaler..." -ForegroundColor White
kubectl delete hpa webapp-hpa

Write-Host "Deleting Web Application Service..." -ForegroundColor White
kubectl delete service webapp-service

Write-Host "Deleting Web Application Deployment..." -ForegroundColor White
kubectl delete deployment webapp-deployment

Write-Host "Deleting MongoDB Service..." -ForegroundColor White
kubectl delete service mongodb-service

Write-Host "Deleting MongoDB Deployment..." -ForegroundColor White
kubectl delete deployment mongodb-deployment

Write-Host "Deleting MongoDB Persistent Volume Claim..." -ForegroundColor White
kubectl delete pvc mongodb-pvc

Write-Host ""
Write-Host "Alternative: Delete all resources using YAML file" -ForegroundColor Gray
Write-Host "kubectl delete -f k8s-deploy-all.yaml" -ForegroundColor Gray

# ============================================================================
# STEP 2: VERIFY CLEANUP
# ============================================================================
Write-Host ""
Write-Host "STEP 2: Verifying Resource Cleanup" -ForegroundColor Cyan

Write-Host "Checking remaining pods..." -ForegroundColor White
kubectl get pods

Write-Host "Checking remaining services..." -ForegroundColor White
kubectl get services

Write-Host "Checking remaining PVCs..." -ForegroundColor White
kubectl get pvc

Write-Host "Checking remaining deployments..." -ForegroundColor White
kubectl get deployments

# ============================================================================
# STEP 3: FORCE DELETE ANY STUCK RESOURCES
# ============================================================================
Write-Host ""
Write-Host "STEP 3: Force Delete Any Stuck Resources (if needed)" -ForegroundColor Cyan

Write-Host "Force deleting any remaining pods..." -ForegroundColor White
kubectl delete pods --all --force --grace-period=0

Write-Host "Force deleting any remaining PVCs..." -ForegroundColor White
kubectl delete pvc --all --force --grace-period=0

# ============================================================================
# STEP 4: CLEAN UP DOCKER IMAGES IN MINIKUBE
# ============================================================================
Write-Host ""
Write-Host "STEP 4: Cleaning Up Docker Images" -ForegroundColor Cyan

Write-Host "Removing custom application image from minikube..." -ForegroundColor White
minikube image rm service-provider-web:latest

Write-Host "Listing remaining images..." -ForegroundColor White
minikube image ls

# ============================================================================
# STEP 5: STOP MINIKUBE
# ============================================================================
Write-Host ""
Write-Host "STEP 5: Stopping Minikube" -ForegroundColor Cyan

Write-Host "Stopping minikube cluster..." -ForegroundColor White
minikube stop

Write-Host "Checking minikube status..." -ForegroundColor White
minikube status

# ============================================================================
# OPTIONAL: COMPLETE MINIKUBE DELETION
# ============================================================================
Write-Host ""
Write-Host "OPTIONAL: Complete Minikube Deletion" -ForegroundColor Cyan
Write-Host "The following commands will completely remove minikube:" -ForegroundColor Yellow
Write-Host ""
Write-Host "# Delete the entire minikube cluster" -ForegroundColor Gray
Write-Host "minikube delete" -ForegroundColor Red
Write-Host ""
Write-Host "# Remove all minikube data" -ForegroundColor Gray
Write-Host "minikube delete --all" -ForegroundColor Red

$deleteCluster = Read-Host "Do you want to completely delete the minikube cluster? (y/N)"
if ($deleteCluster -eq 'y' -or $deleteCluster -eq 'Y') {
    Write-Host "Deleting minikube cluster..." -ForegroundColor Red
    minikube delete
} else {
    Write-Host "Minikube cluster kept (stopped but not deleted)" -ForegroundColor Green
}

# ============================================================================
# CLEANUP SUMMARY
# ============================================================================
Write-Host ""
Write-Host "=== Cleanup Summary ===" -ForegroundColor Green
Write-Host "✅ Kubernetes resources deleted" -ForegroundColor White
Write-Host "✅ Docker images removed from minikube" -ForegroundColor White
Write-Host "✅ Minikube cluster stopped" -ForegroundColor White
if ($deleteCluster -eq 'y' -or $deleteCluster -eq 'Y') {
    Write-Host "✅ Minikube cluster deleted" -ForegroundColor White
} else {
    Write-Host "ℹ️  Minikube cluster stopped but not deleted" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Cleanup completed!" -ForegroundColor Green
Write-Host "Cleanup performed on: $(Get-Date)" -ForegroundColor Gray 