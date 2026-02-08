# Kubernetes Local Deployment Guide

This guide provides step-by-step instructions for deploying the Todo Chatbot application on a local Minikube cluster.

## Prerequisites

- [Docker](https://www.docker.com/) installed and running
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed
- [Helm 3.x](https://helm.sh/docs/intro/install/) installed
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed

## Quick Start (Automated)

### Windows
```cmd
deploy-local.bat
```

### Linux/Mac
```bash
chmod +x deploy-local.sh
./deploy-local.sh
```

## Manual Deployment Steps

### Step 1: Start Minikube

```bash
# Start Minikube with recommended settings
minikube start --cpus=4 --memory=4096

# Verify Minikube is running
minikube status
```

### Step 2: Build Docker Images

```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .

# Build frontend image
cd ../frontend
docker build -t todo-frontend:latest .

# Return to project root
cd ..
```

### Step 3: Load Images into Minikube

Since we're using local images, we need to load them into Minikube's Docker daemon:

```bash
# Load backend image
minikube image load todo-backend:latest

# Load frontend image
minikube image load todo-frontend:latest

# Verify images are loaded
minikube image ls | grep todo
```

### Step 4: Enable NGINX Ingress Controller

```bash
# Enable ingress addon
minikube addons enable ingress

# Verify ingress controller is running
kubectl get pods -n ingress-nginx
```

### Step 5: Deploy with Helm

```bash
# Install the Helm chart with local development values
helm install todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-chatbot --timeout=300s
```

### Step 6: Verify Deployment

```bash
# Check all resources
kubectl get all

# Check pods status
kubectl get pods

# Check services
kubectl get svc

# Check ingress
kubectl get ingress

# Check persistent volume claims
kubectl get pvc
```

### Step 7: Access the Application

#### Option 1: NodePort (Recommended for Minikube)

```bash
# Get Minikube IP
minikube ip

# Access the application at:
# http://<MINIKUBE_IP>:30080
```

For example, if Minikube IP is `192.168.49.2`, access at `http://192.168.49.2:30080`

#### Option 2: Ingress

```bash
# Get Minikube IP
minikube ip

# Add to hosts file:
# Linux/Mac: /etc/hosts
# Windows: C:\Windows\System32\drivers\etc\hosts
# Add line: <MINIKUBE_IP> todo-app.local

# Access at: http://todo-app.local
```

#### Option 3: Port Forwarding

```bash
# Forward frontend port
kubectl port-forward svc/todo-chatbot-frontend 3000:3000

# Access at: http://localhost:3000
```

## Updating the Application

### Update Docker Images

```bash
# Rebuild images
cd backend && docker build -t todo-backend:latest . && cd ..
cd frontend && docker build -t todo-frontend:latest . && cd ..

# Reload images into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Restart pods to use new images
kubectl rollout restart deployment/todo-chatbot-backend
kubectl rollout restart deployment/todo-chatbot-frontend

# Watch rollout status
kubectl rollout status deployment/todo-chatbot-backend
kubectl rollout status deployment/todo-chatbot-frontend
```

### Update Helm Configuration

```bash
# Upgrade the Helm release
helm upgrade todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml

# Or force upgrade with cleanup
helm upgrade todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml --force
```

## Debugging Commands

### View Logs

```bash
# Backend logs
kubectl logs -l app.kubernetes.io/component=backend -f

# Frontend logs
kubectl logs -l app.kubernetes.io/component=frontend -f

# Specific pod logs
kubectl logs <pod-name> -f
```

### Inspect Resources

```bash
# Describe pod (shows events and status)
kubectl describe pod <pod-name>

# Describe service
kubectl describe svc <service-name>

# Describe ingress
kubectl describe ingress todo-chatbot

# View events
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Execute Commands in Pods

```bash
# Get shell access to backend pod
kubectl exec -it <backend-pod-name> -- /bin/sh

# Get shell access to frontend pod
kubectl exec -it <frontend-pod-name> -- /bin/sh

# Run a specific command
kubectl exec <pod-name> -- <command>
```

### Test Backend Health

```bash
# Create a temporary pod to test connectivity
kubectl run curl --image=curlimages/curl -i --tty --rm -- sh

# Inside the pod, test backend
curl http://todo-chatbot-backend:8000/health
```

### Check Resource Usage

```bash
# View resource usage for all pods
kubectl top pods

# View resource usage for nodes
kubectl top nodes
```

## Common Issues and Solutions

### Issue 1: ImagePullBackOff Error

**Problem**: Pods show `ImagePullBackOff` status

**Solution**:
```bash
# Make sure images are loaded in Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Verify imagePullPolicy is "Never" in values-local.yaml
# Restart the deployment
kubectl rollout restart deployment/todo-chatbot-backend
kubectl rollout restart deployment/todo-chatbot-frontend
```

### Issue 2: Cannot Access via Ingress

**Problem**: Ingress host is not accessible

**Solution**:
```bash
# Check if ingress addon is enabled
minikube addons list | grep ingress

# If not enabled, enable it
minikube addons enable ingress

# Verify ingress controller pods are running
kubectl get pods -n ingress-nginx

# Check ingress configuration
kubectl describe ingress todo-chatbot

# Ensure hosts file has correct entry
minikube ip  # Use this IP in hosts file
```

### Issue 3: Pods Not Starting (CrashLoopBackOff)

**Problem**: Pods keep restarting

**Solution**:
```bash
# Check pod logs for errors
kubectl logs <pod-name>

# Check pod events
kubectl describe pod <pod-name>

# Common fixes:
# - Check environment variables in values-local.yaml
# - Verify health check endpoints are correct
# - Check resource limits (CPU/memory)
```

### Issue 4: Database Persistence Issues

**Problem**: Data is lost after pod restart

**Solution**:
```bash
# Check PVC status
kubectl get pvc

# Check if PVC is bound
kubectl describe pvc todo-chatbot-backend-pvc

# If not bound, check storage class
kubectl get sc

# Verify persistence is enabled in values-local.yaml
```

### Issue 5: Frontend Cannot Connect to Backend

**Problem**: Frontend shows API connection errors

**Solution**:
```bash
# Verify backend service is running
kubectl get svc todo-chatbot-backend

# Check backend logs for errors
kubectl logs -l app.kubernetes.io/component=backend

# Test backend connectivity from frontend pod
kubectl exec <frontend-pod> -- curl http://todo-chatbot-backend:8000/health

# Verify environment variables in frontend deployment
kubectl describe deployment todo-chatbot-frontend
```

## Cleanup

### Uninstall the Application

```bash
# Uninstall Helm release
helm uninstall todo-chatbot

# Verify all resources are deleted
kubectl get all

# Delete PVC if needed (this will delete data!)
kubectl delete pvc todo-chatbot-backend-pvc
```

### Stop Minikube

```bash
# Stop Minikube
minikube stop

# Delete Minikube cluster (WARNING: Deletes all data!)
minikube delete
```

## Helm Chart Structure

```
todo-chatbot/
├── Chart.yaml                      # Chart metadata
├── values.yaml                     # Default values
├── values-local.yaml               # Local development values
├── README.md                       # Chart documentation
└── templates/
    ├── _helpers.tpl                # Template helpers
    ├── backend-deployment.yaml     # Backend deployment
    ├── backend-service.yaml        # Backend service
    ├── frontend-deployment.yaml    # Frontend deployment
    ├── frontend-service.yaml       # Frontend service
    ├── configmap.yaml              # Configuration
    ├── pvc.yaml                    # Persistent volume claim
    ├── ingress.yaml                # Ingress rules
    ├── serviceaccount.yaml         # Service account
    ├── hpa.yaml                    # Horizontal pod autoscaler
    ├── deployment.yaml.old         # Original template (backup)
    └── service.yaml.old            # Original template (backup)
```

## Configuration Options

### Key Values in values-local.yaml

```yaml
backend:
  image:
    pullPolicy: Never              # Use local images
  service:
    type: ClusterIP               # Internal only
    port: 8000
  env:
    DATABASE_URL: "sqlite:///./data/todo_app.db"
    ENVIRONMENT: "development"

frontend:
  image:
    pullPolicy: Never              # Use local images
  service:
    type: NodePort                # Accessible from outside
    port: 3000
    nodePort: 30080               # Fixed external port

persistence:
  enabled: true                    # Enable data persistence
  size: 1Gi

ingress:
  enabled: true
  className: "nginx"
```

## Production Considerations

When deploying to production, consider:

1. **Use external database** (PostgreSQL/MySQL) instead of SQLite
2. **Configure secrets** properly (use Kubernetes Secrets)
3. **Set proper resource limits** based on load testing
4. **Enable TLS/SSL** for ingress
5. **Use external image registry** (DockerHub, ECR, GCR)
6. **Configure autoscaling** (HPA)
7. **Set up monitoring** (Prometheus, Grafana)
8. **Configure backup** for persistent data
9. **Use proper storage class** for your cloud provider
10. **Implement health checks** and readiness probes

## Additional Resources

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Documentation](https://minikube.sigs.k8s.io/docs/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
