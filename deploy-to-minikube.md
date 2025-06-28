# Deploying Service Provider Web Application to Minikube

## Prerequisites
- Docker Desktop installed and running
- Minikube installed and started
- kubectl installed

## Step 1: Start Minikube and Enable Required Add-ons

```bash
# Start minikube
minikube start

# Enable metrics server for HPA
minikube addons enable metrics-server

# Enable ingress (optional, for advanced load balancing)
minikube addons enable ingress

# Verify minikube is running
minikube status
```

## Step 2: Build Docker Image

```bash
# Build the web application Docker image
docker build -t service-provider-web:latest .

# Load the image into minikube
minikube image load service-provider-web:latest

# Verify the image is loaded
minikube image ls | grep service-provider-web
```

## Step 3: Deploy to Kubernetes

### Option A: Deploy all components at once
```bash
kubectl apply -f k8s-deploy-all.yaml
```

### Option B: Deploy components individually
```bash
# Deploy MongoDB components
kubectl apply -f k8s-mongodb-pvc.yaml
kubectl apply -f k8s-mongodb-deployment.yaml
kubectl apply -f k8s-mongodb-service.yaml

# Wait for MongoDB to be ready
kubectl wait --for=condition=available --timeout=300s deployment/mongodb-deployment

# Deploy Web Application components
kubectl apply -f k8s-webapp-deployment.yaml
kubectl apply -f k8s-webapp-service.yaml
kubectl apply -f k8s-webapp-hpa.yaml
```

## Step 4: Verify Deployment

```bash
# Check all pods are running
kubectl get pods

# Check services
kubectl get services

# Check persistent volume claims
kubectl get pvc

# Check horizontal pod autoscaler
kubectl get hpa

# Get detailed information about deployments
kubectl get deployments -o wide
```

## Step 5: Access the Application

```bash
# Get the external IP for the LoadBalancer service
minikube service webapp-service --url

# Or use port forwarding
kubectl port-forward service/webapp-service 8080:80
```

Then access your application at the provided URL or `http://localhost:8080`

## Step 6: Monitor and Test Auto-scaling

```bash
# Watch HPA status
kubectl get hpa webapp-hpa --watch

# Generate load to test auto-scaling (in a new terminal)
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh
# Inside the pod, run:
while true; do wget -q -O- http://webapp-service; done
```

## Step 7: Clean Up (Optional)

```bash
# Delete all resources
kubectl delete -f k8s-deploy-all.yaml

# Or delete individually
kubectl delete hpa webapp-hpa
kubectl delete service webapp-service
kubectl delete deployment webapp-deployment
kubectl delete service mongodb-service
kubectl delete deployment mongodb-deployment
kubectl delete pvc mongodb-pvc
```

## Troubleshooting

### Check Pod Logs
```bash
# Get pod logs for web application
kubectl logs -l app=webapp

# Get pod logs for MongoDB
kubectl logs -l app=mongodb

# Follow logs in real-time
kubectl logs -f deployment/webapp-deployment
```

### Debug Pods
```bash
# Describe a pod to see events
kubectl describe pod <pod-name>

# Get pod status
kubectl get pods -o wide

# Execute commands inside a pod
kubectl exec -it <pod-name> -- /bin/bash
```

### Check Resource Usage
```bash
# Check node resource usage
kubectl top nodes

# Check pod resource usage
kubectl top pods
```

## Application Components

### Database (MongoDB)
- **Deployment**: `mongodb-deployment` (1 replica)
- **Service**: `mongodb-service` (NodePort on 30017)
- **Storage**: 5Gi persistent volume
- **Resources**: 512Mi-1Gi RAM, 250m-500m CPU

### Web Application (FastAPI)
- **Deployment**: `webapp-deployment` (3 replicas, scalable 3-10)
- **Service**: `webapp-service` (LoadBalancer on port 80)
- **Auto-scaling**: Based on CPU (70%) and Memory (80%) utilization
- **Resources**: 256Mi-512Mi RAM, 200m-500m CPU
- **Health Checks**: Liveness and readiness probes on `/homepage`

## Key Features Implemented

✅ **Multiple replicas of web servers** (3 replicas, scalable to 10)
✅ **Single database server replica** with persistent storage
✅ **LoadBalancer service** for web server
✅ **NodePort service** for database server
✅ **Persistent Volume Claim** for database data persistence
✅ **HorizontalPodAutoscaler** for automatic scaling based on traffic
✅ **Resource limits and requests** for optimal resource management
✅ **Health checks** for application reliability 