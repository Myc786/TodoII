# Todo Chatbot Helm Chart

A Helm chart for deploying the Todo Chatbot application on Kubernetes. This chart deploys both the FastAPI backend and Next.js frontend services.

## Prerequisites

- Kubernetes cluster (Minikube for local development)
- Helm 3.x
- Docker images built:
  - `todo-backend:latest`
  - `todo-frontend:latest`

## Quick Start for Local Development

### 1. Build Docker Images

```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .

# Build frontend image
cd ../frontend
docker build -t todo-frontend:latest .
```

### 2. Load Images into Minikube

```bash
# Start Minikube if not already running
minikube start

# Load images into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Verify images are loaded
minikube image ls | grep todo
```

### 3. Enable NGINX Ingress Controller

```bash
minikube addons enable ingress
```

### 4. Install the Helm Chart

```bash
# Install with local development values
helm install todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml

# Or upgrade if already installed
helm upgrade todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml
```

### 5. Access the Application

#### Option 1: Using NodePort (Recommended for Minikube)

```bash
# Get Minikube IP
minikube ip

# Access frontend at: http://<MINIKUBE_IP>:30080
```

#### Option 2: Using Ingress

```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts (Linux/Mac) or C:\Windows\System32\drivers\etc\hosts (Windows)
<MINIKUBE_IP> todo-app.local

# Access at: http://todo-app.local
```

#### Option 3: Using Port Forwarding

```bash
# Forward frontend port
kubectl port-forward svc/todo-chatbot-frontend 3000:3000

# Forward backend port
kubectl port-forward svc/todo-chatbot-backend 8000:8000

# Access at: http://localhost:3000
```

## Configuration

### Key Configuration Files

- `values.yaml` - Default values for production deployment
- `values-local.yaml` - Values optimized for local Minikube development

### Key Configuration Options

#### Backend Configuration

```yaml
backend:
  enabled: true
  replicaCount: 1
  image:
    repository: todo-backend
    pullPolicy: Never  # Use "Never" for Minikube local images
    tag: "latest"
  service:
    type: ClusterIP
    port: 8000
  env:
    DATABASE_URL: "sqlite:///./data/todo_app.db"
    ENVIRONMENT: "development"
    # ... other environment variables
```

#### Frontend Configuration

```yaml
frontend:
  enabled: true
  replicaCount: 1
  image:
    repository: todo-frontend
    pullPolicy: Never  # Use "Never" for Minikube local images
    tag: "latest"
  service:
    type: NodePort
    port: 3000
    nodePort: 30080  # Fixed port for easy access
  env:
    NEXT_PUBLIC_API_URL: "http://todo-app.local/api"
    # ... other environment variables
```

#### Persistence

```yaml
persistence:
  enabled: true
  storageClass: "standard"
  accessMode: ReadWriteOnce
  size: 1Gi
```

## Useful Commands

### Helm Commands

```bash
# Install chart
helm install todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml

# Upgrade chart
helm upgrade todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml

# Uninstall chart
helm uninstall todo-chatbot

# View rendered templates (dry-run)
helm install todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml --dry-run --debug

# List releases
helm list

# Get release status
helm status todo-chatbot
```

### Kubernetes Commands

```bash
# Get all resources
kubectl get all

# Get pods
kubectl get pods

# Get services
kubectl get svc

# Get ingress
kubectl get ingress

# View logs for backend
kubectl logs -l app.kubernetes.io/component=backend -f

# View logs for frontend
kubectl logs -l app.kubernetes.io/component=frontend -f

# Describe pod (for troubleshooting)
kubectl describe pod <pod-name>

# Get pod shell access
kubectl exec -it <pod-name> -- /bin/sh

# View persistent volume claims
kubectl get pvc
```

### Debugging

```bash
# Check if images are loaded in Minikube
minikube image ls | grep todo

# Check pod events
kubectl get events --sort-by=.metadata.creationTimestamp

# Check if services are running
kubectl get svc

# Test backend health endpoint
kubectl run curl --image=curlimages/curl -i --tty --rm -- curl http://todo-chatbot-backend:8000/health

# Check ingress configuration
kubectl describe ingress todo-chatbot
```

## Architecture

### Components

1. **Backend Service** (`todo-chatbot-backend`)
   - FastAPI application
   - Port: 8000
   - Health check endpoint: `/health`
   - Database: SQLite with persistent volume

2. **Frontend Service** (`todo-chatbot-frontend`)
   - Next.js application
   - Port: 3000
   - Connects to backend via internal Kubernetes service

3. **Persistent Volume**
   - Used for SQLite database storage
   - Size: 1Gi
   - StorageClass: standard (Minikube default)

4. **Ingress** (Optional)
   - Routes traffic to frontend and backend
   - Path-based routing:
     - `/` → frontend
     - `/api` → backend

### Network Flow

```
User → NodePort (30080) → Frontend Service (3000)
                           ↓
Frontend → Backend Service (8000) → Database (PVC)
```

## Troubleshooting

### Pods not starting (ImagePullBackOff)

```bash
# Make sure images are loaded in Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Verify pullPolicy is set to "Never" in values-local.yaml
```

### Cannot access via Ingress

```bash
# Ensure ingress addon is enabled
minikube addons enable ingress

# Check ingress status
kubectl get ingress
kubectl describe ingress todo-chatbot

# Verify /etc/hosts entry matches Minikube IP
minikube ip
```

### Database persistence issues

```bash
# Check PVC status
kubectl get pvc

# Check PV status
kubectl get pv

# Describe PVC for details
kubectl describe pvc todo-chatbot-backend-pvc
```

### Backend health check failing

```bash
# Check backend logs
kubectl logs -l app.kubernetes.io/component=backend

# Check if health endpoint is accessible
kubectl exec -it <backend-pod> -- curl localhost:8000/health
```

## Production Deployment

For production deployment, use the default `values.yaml` and adjust:

1. Set proper image repositories and tags
2. Configure proper secrets for JWT keys
3. Enable TLS/SSL for ingress
4. Configure external database (PostgreSQL recommended)
5. Adjust resource limits based on load
6. Enable autoscaling if needed
7. Configure proper storage class for your cloud provider

Example:

```bash
helm install todo-chatbot ./todo-chatbot \
  --set backend.image.repository=myregistry.io/todo-backend \
  --set backend.image.tag=v1.0.0 \
  --set frontend.image.repository=myregistry.io/todo-frontend \
  --set frontend.image.tag=v1.0.0 \
  --set ingress.hosts[0].host=todo.example.com \
  --set ingress.tls[0].secretName=todo-tls
```

## Support

For issues and questions, please open an issue in the repository.
