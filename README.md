# AutoScale – Kubernetes-Based Automatic Scaling System

A production-ready demonstration of Kubernetes Horizontal Pod Autoscaler (HPA) using Python Flask, Docker, and Kubernetes Metrics Server.

---

## 1. Architecture Overview

```text
[ Incoming Traffic / Load Generator ]
                  |
                  v
       [ Kubernetes Service ] (NodePort: 30080)
                  |
        ---------------------
        |                   |
  [ Pod 1 (App) ]     [ Pod 2 (App) ]  <--- (Scales 2 to 10 Pods)
        \                   /
         [ Metrics Server ]
                  |
       [ Horizontal Pod Autoscaler ] (Target CPU: 50%)
```

---

## 2. Project Directory Structure

```text
AutoScale/
├── app/
│   ├── app.py                # Flask application with /heavy, /health, /status endpoints
│   └── requirements.txt      # Gunicorn and Flask dependencies
├── docker/
│   └── Dockerfile            # Multi-worker Python 3.11-slim container image
├── kubernetes/
│   ├── deployment.yaml       # Deployment with 2 initial replicas and resource limits
│   ├── service.yaml          # NodePort Service exposing application
│   └── hpa.yaml              # HPA configured for 50% CPU threshold (min: 2, max: 10)
├── testing/
│   └── load_generator.py     # Concurrent multi-threaded load generator
└── README.md
```

---

## 3. Quickstart & Deployment

### Step 1: Start Minikube & Enable Metrics Server
```bash
# Start Minikube with resources optimized for ~7GB laptops
minikube start --driver=docker --cpus=2 --memory=2800m

# Enable the Metrics Server addon
minikube addons enable metrics-server
```

### Step 2: Build the Container Image directly into Minikube
```bash
# Point your Docker CLI to Minikube's Docker daemon
eval $(minikube docker-env)

# Build the image inside Minikube
docker build -t autoscale-app:v1 -f docker/Dockerfile .
```

### Step 3: Deploy to Kubernetes
```bash
# Deploy Deployment, Service, and HPA
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
kubectl apply -f kubernetes/hpa.yaml

# Verify initial status (2 Pods running)
kubectl get pods -l app=autoscale-app
kubectl get hpa autoscale-hpa
```

---

## 4. Demonstrating Auto-Scaling

### 1. Open live monitors in separate terminals
```bash
# Watch HPA metrics and target utilization
kubectl get hpa autoscale-hpa -w
```
```bash
# Watch Pods scaling up and down in real-time
kubectl get pods -l app=autoscale-app -w
```

### 2. Run the Load Generator
Get the URL of the service:
```bash
export APP_URL=$(minikube service autoscale-service --url)
python3 testing/load_generator.py "$APP_URL/heavy?iterations=4000000" 15 120
```

### 3. Observe the Results
- **Scale Up:** As CPU surpasses 50%, HPA will scale replicas: `2 -> 4 -> 6 -> 8 -> 10`.
- **Scale Down:** Once traffic stops, CPU drops below 50% and HPA scales back down to 2 replicas safely.
