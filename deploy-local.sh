#!/bin/bash

# Todo Chatbot - Local Deployment Script for Minikube
# This script automates the deployment process for local development

set -e  # Exit on error

echo "========================================="
echo "Todo Chatbot - Local Deployment Script"
echo "========================================="
echo ""

# Check if Minikube is running
echo "1. Checking Minikube status..."
if ! minikube status > /dev/null 2>&1; then
    echo "   ⚠️  Minikube is not running. Starting Minikube..."
    minikube start
else
    echo "   ✓ Minikube is running"
fi
echo ""

# Check if images exist
echo "2. Checking Docker images..."
if ! docker image inspect todo-backend:latest > /dev/null 2>&1; then
    echo "   ⚠️  Backend image not found. Building..."
    cd backend
    docker build -t todo-backend:latest .
    cd ..
else
    echo "   ✓ Backend image exists"
fi

if ! docker image inspect todo-frontend:latest > /dev/null 2>&1; then
    echo "   ⚠️  Frontend image not found. Building..."
    cd frontend
    docker build -t todo-frontend:latest .
    cd ..
else
    echo "   ✓ Frontend image exists"
fi
echo ""

# Load images into Minikube
echo "3. Loading images into Minikube..."
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
echo "   ✓ Images loaded into Minikube"
echo ""

# Enable ingress addon
echo "4. Enabling NGINX Ingress Controller..."
if minikube addons list | grep -q "ingress: enabled"; then
    echo "   ✓ Ingress addon already enabled"
else
    minikube addons enable ingress
    echo "   ✓ Ingress addon enabled"
fi
echo ""

# Deploy or upgrade Helm chart
echo "5. Deploying Helm chart..."
if helm list | grep -q "todo-chatbot"; then
    echo "   Upgrading existing release..."
    helm upgrade todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml
else
    echo "   Installing new release..."
    helm install todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml
fi
echo "   ✓ Helm chart deployed"
echo ""

# Wait for pods to be ready
echo "6. Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-chatbot --timeout=300s
echo "   ✓ All pods are ready"
echo ""

# Get access information
echo "========================================="
echo "Deployment Complete!"
echo "========================================="
echo ""

MINIKUBE_IP=$(minikube ip)
echo "Access your application:"
echo ""
echo "1. NodePort (Recommended):"
echo "   Frontend: http://$MINIKUBE_IP:30080"
echo ""
echo "2. Ingress (Add to /etc/hosts first):"
echo "   Add this line to your hosts file:"
echo "   $MINIKUBE_IP todo-app.local"
echo "   Then access: http://todo-app.local"
echo ""
echo "3. Port Forward:"
echo "   Run: kubectl port-forward svc/todo-chatbot-frontend 3000:3000"
echo "   Then access: http://localhost:3000"
echo ""
echo "Useful commands:"
echo "  - View pods: kubectl get pods"
echo "  - View services: kubectl get svc"
echo "  - View logs (backend): kubectl logs -l app.kubernetes.io/component=backend -f"
echo "  - View logs (frontend): kubectl logs -l app.kubernetes.io/component=frontend -f"
echo "  - Uninstall: helm uninstall todo-chatbot"
echo ""
