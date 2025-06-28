# DevOps Assignment Report: Kubernetes Deployment
## CLO-5: Deploying Web Application over Kubernetes Cluster

**Student Name:** [Your Name]  
**Course:** DevOps  
**Assignment:** Kubernetes Deployment with Minikube  
**Date:** [Current Date]

---

## Table of Contents
1. [Assignment Overview](#assignment-overview)
2. [Application Description](#application-description)
3. [Prerequisites and Setup](#prerequisites-and-setup)
4. [Docker Configuration](#docker-configuration)
5. [Kubernetes YAML Files](#kubernetes-yaml-files)
6. [Deployment Process](#deployment-process)
7. [Troubleshooting](#troubleshooting)
8. [Results and Verification](#results-and-verification)
9. [Key Features Implemented](#key-features-implemented)
10. [Conclusion](#conclusion)

---

## Assignment Overview

The objective of this assignment was to deploy a web application on a Kubernetes cluster using minikube. The application consists of:

- **Web Server**: FastAPI-based service provider application with multiple replicas
- **Database Server**: MongoDB with persistent storage
- **Load Balancing**: LoadBalancer service for the web server
- **Auto-scaling**: HorizontalPodAutoscaler for dynamic scaling
- **Persistent Storage**: PersistentVolumeClaim for database data

### Requirements Met:
✅ Multiple replicas of web servers (3-10 replicas)  
✅ Single database server replica with persistent storage  
✅ LoadBalancer service for web server  
✅ NodePort service for database server  
✅ PersistentVolumeClaim for database persistence  
✅ HorizontalPodAutoscaler for auto-scaling  
✅ Well-indented YAML files  

---

## Application Description

### Service Provider Web Application
- **Framework**: FastAPI (Python)
- **Database**: MongoDB
- **Features**: 
  - User authentication and registration
  - Service booking system
  - Admin dashboard
  - Multiple service categories (automotive, home services, personal services)
  - File upload functionality
  - Contact form and notifications

### Architecture Components
- **Frontend**: HTML templates with Jinja2
- **Backend**: FastAPI with async/await support
- **Database**: MongoDB for data persistence
- **Authentication**: BCrypt password hashing
- **File Handling**: Static file serving and uploads

---

## Prerequisites and Setup

### Software Requirements
- Docker Desktop (installed and running)
- Minikube (lightweight Kubernetes implementation)
- kubectl (Kubernetes command-line tool)
- Windows PowerShell

### Initial Setup Commands
```powershell
# Start minikube
minikube start

# Enable required addons
minikube addons enable metrics-server
minikube addons enable ingress

# Verify minikube status
minikube status
```

---

## Docker Configuration

### Dockerfile
```dockerfile
# Use Python 3.12 as base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create directory for uploaded files
RUN mkdir -p /app/static/uploads

# Expose port 8000 (FastAPI default port)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Building and Loading Docker Image
```powershell
# Build the Docker image
docker build -t service-provider-web:latest .

# Load image into minikube
minikube image load service-provider-web:latest

# Verify image is loaded
minikube image ls | findstr service-provider
```

---

## Kubernetes YAML Files

### 1. MongoDB Persistent Volume Claim
**File:** `k8s-mongodb-pvc.yaml`
```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mongodb-pvc
  labels:
    app: mongodb
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
  storageClassName: standard
```

### 2. MongoDB Deployment
**File:** `k8s-mongodb-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongodb-deployment
  labels:
    app: mongodb
spec:
  replicas: 1
  selector:
    matchLabels:
      app: mongodb
  template:
    metadata:
      labels:
        app: mongodb
    spec:
      containers:
      - name: mongodb
        image: mongo:latest
        ports:
        - containerPort: 27017
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          value: ""
        - name: MONGO_INITDB_ROOT_PASSWORD
          value: ""
        volumeMounts:
        - name: mongodb-storage
          mountPath: /data/db
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
      volumes:
      - name: mongodb-storage
        persistentVolumeClaim:
          claimName: mongodb-pvc
```

### 3. MongoDB Service (NodePort)
**File:** `k8s-mongodb-service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: mongodb-service
  labels:
    app: mongodb
spec:
  type: NodePort
  ports:
  - port: 27017
    targetPort: 27017
    nodePort: 30017
  selector:
    app: mongodb
```

### 4. Web Application Deployment
**File:** `k8s-webapp-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: webapp-deployment
  labels:
    app: webapp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: webapp
  template:
    metadata:
      labels:
        app: webapp
    spec:
      containers:
      - name: webapp
        image: service-provider-web:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
        env:
        - name: MONGO_URI
          value: "mongodb://mongodb-service:27017"
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /homepage
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /homepage
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 5. Web Application Service (LoadBalancer)
**File:** `k8s-webapp-service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: webapp-service
  labels:
    app: webapp
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
    protocol: TCP
  selector:
    app: webapp
```

### 6. HorizontalPodAutoscaler
**File:** `k8s-webapp-hpa.yaml`
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: webapp-hpa
  labels:
    app: webapp
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: webapp-deployment
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
      - type: Percent
        value: 100
        periodSeconds: 15
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
      - type: Percent
        value: 10
        periodSeconds: 60
```

---

## Deployment Process

### Step 1: Environment Preparation
```powershell
# Start minikube and enable addons
minikube start
minikube addons enable metrics-server
minikube addons enable ingress
```

### Step 2: Build and Load Docker Image
```powershell
# Build the application image
docker build -t service-provider-web:latest .

# Load image into minikube's Docker daemon
minikube image load service-provider-web:latest
```

### Step 3: Deploy to Kubernetes
```powershell
# Deploy all components at once
kubectl apply -f k8s-deploy-all.yaml
```

**Output:**
```
persistentvolumeclaim/mongodb-pvc created
deployment.apps/mongodb-deployment created
service/mongodb-service created
deployment.apps/webapp-deployment created
service/webapp-service created
horizontalpodautoscaler.autoscaling/webapp-hpa created
```

### Step 4: Verify Deployment
```powershell
# Check pod status
kubectl get pods

# Check services
kubectl get services

# Check PVC
kubectl get pvc

# Check HPA
kubectl get hpa
```

---

## Troubleshooting

### Issue Encountered: ImagePullBackOff Error

**Problem:** The webapp pods were failing with `ImagePullBackOff` status.

**Root Cause Analysis:**
```powershell
kubectl describe pod webapp-deployment-6676c5ddc7-r4bgq
```

**Error Details:**
```
Failed to pull image "service-provider-web:latest": Error response from daemon: 
pull access denied for service-provider-web, repository does not exist or may 
require 'docker login': denied: requested access to the resource is denied
```

**Solution Applied:**
Added `imagePullPolicy: Never` to the webapp deployment to force Kubernetes to use the locally loaded image instead of trying to pull from a remote registry.

**Fixed YAML Section:**
```yaml
containers:
- name: webapp
  image: service-provider-web:latest
  imagePullPolicy: Never  # Added this line
  ports:
  - containerPort: 8000
```

**Fix Commands:**
```powershell
# Apply the corrected deployment
kubectl apply -f k8s-webapp-deployment.yaml
```

---

## Results and Verification

### Final Pod Status
```powershell
PS C:\Khizar\7th Semester\Devops\project\service-provider> kubectl get pods
NAME                                 READY   STATUS    RESTARTS   AGE
mongodb-deployment-cf49cbc4d-krf75   1/1     Running   0          3m1s
webapp-deployment-d6884db58-h6c9g    1/1     Running   0          11s
webapp-deployment-d6884db58-rt2kk    1/1     Running   0          26s
webapp-deployment-d6884db58-z5lrr    1/1     Running   0          18s
```

### Service Status
```powershell
PS C:\Khizar\7th Semester\Devops\project\service-provider> kubectl get services
NAME              TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)           AGE
kubernetes        ClusterIP      10.96.0.1        <none>        443/TCP           4m23s
mongodb-service   NodePort       10.105.156.242   <none>        27017:30017/TCP   59s
webapp-service    LoadBalancer   10.98.215.146    <pending>     80:30523/TCP      59s
```

### Application Access
```powershell
# Get application URL
minikube service webapp-service --url
```

**Note:** The LoadBalancer service shows `<pending>` for EXTERNAL-IP because minikube runs locally. Access is provided through the minikube service command.

---

## Key Features Implemented

### 1. **Multiple Web Server Replicas**
- **Implementation**: 3 initial replicas in webapp-deployment
- **Scaling**: Auto-scalable from 3 to 10 replicas via HPA
- **Load Distribution**: Handled by LoadBalancer service

### 2. **Single Database Server with Persistence**
- **Implementation**: 1 replica MongoDB deployment
- **Storage**: 5Gi PersistentVolumeClaim
- **Data Persistence**: Survives pod restarts and rescheduling

### 3. **Service Types Implementation**
- **Web Server**: LoadBalancer service on port 80
- **Database**: NodePort service on port 30017
- **Internal Communication**: ClusterIP for internal traffic

### 4. **Auto-scaling Configuration**
- **CPU Threshold**: 70% utilization
- **Memory Threshold**: 80% utilization
- **Scale Range**: 3-10 replicas
- **Behavior**: Controlled scale-up/down policies

### 5. **Health Monitoring**
- **Liveness Probe**: HTTP GET on `/homepage` endpoint
- **Readiness Probe**: Ensures pod is ready to receive traffic
- **Resource Limits**: Defined CPU and memory constraints

### 6. **Environment Configuration**
- **Database Connection**: MongoDB URI via environment variables
- **Container Networking**: Service discovery through DNS
- **Security**: No hardcoded credentials

---

## Monitoring and Maintenance Commands

### Monitoring Pods
```powershell
# Watch pod status in real-time
kubectl get pods --watch

# Check resource usage
kubectl top pods
kubectl top nodes
```

### Monitoring Auto-scaling
```powershell
# Watch HPA status
kubectl get hpa --watch

# Describe HPA for detailed metrics
kubectl describe hpa webapp-hpa
```

### Log Analysis
```powershell
# View application logs
kubectl logs -l app=webapp

# Follow logs in real-time
kubectl logs -f deployment/webapp-deployment

# View MongoDB logs
kubectl logs -l app=mongodb
```

### Load Testing (for HPA demonstration)
```powershell
# Create a load generator pod
kubectl run -i --tty load-generator --rm --image=busybox --restart=Never -- /bin/sh

# Inside the pod, generate load:
while true; do wget -q -O- http://webapp-service; done
```

---

## Cleanup Commands

```powershell
# Remove all deployed resources
kubectl delete -f k8s-deploy-all.yaml

# Or remove individually
kubectl delete hpa webapp-hpa
kubectl delete service webapp-service
kubectl delete deployment webapp-deployment
kubectl delete service mongodb-service
kubectl delete deployment mongodb-deployment
kubectl delete pvc mongodb-pvc

# Stop minikube
minikube stop
```

---

## Conclusion

This assignment successfully demonstrates the deployment of a containerized web application on a Kubernetes cluster using minikube. The implementation includes:

1. **Containerization**: Successfully dockerized a FastAPI application
2. **Orchestration**: Deployed using Kubernetes with proper resource management
3. **Persistence**: Implemented persistent storage for database data
4. **Scaling**: Configured horizontal pod autoscaling based on resource utilization
5. **Load Balancing**: Implemented LoadBalancer service for traffic distribution
6. **Service Discovery**: Established proper communication between services
7. **Health Monitoring**: Configured liveness and readiness probes
8. **Troubleshooting**: Successfully resolved ImagePullBackOff issues

The deployment showcases enterprise-grade practices including auto-scaling, persistent storage, proper service types, and comprehensive monitoring. The application is now ready for production-like workloads with automatic scaling capabilities based on traffic demands.

### Learning Outcomes Achieved:
✅ Successfully deployed servers on minikube cluster  
✅ Attached persistent volume to database server for persistent storage  
✅ Applied LoadBalancer service for automatic load balancing  
✅ Applied HorizontalPodAutoscaler for auto-scaling of pods  
✅ Gained hands-on experience with Kubernetes YAML configurations  
✅ Learned troubleshooting techniques for container orchestration issues  

---

**End of Report** 