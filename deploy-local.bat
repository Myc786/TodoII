@echo off
REM Todo Chatbot - Local Deployment Script for Minikube (Windows)
REM This script automates the deployment process for local development

echo =========================================
echo Todo Chatbot - Local Deployment Script
echo =========================================
echo.

REM Check if Minikube is running
echo 1. Checking Minikube status...
minikube status >nul 2>&1
if %errorlevel% neq 0 (
    echo    Warning: Minikube is not running. Starting Minikube...
    minikube start
) else (
    echo    OK: Minikube is running
)
echo.

REM Check if images exist
echo 2. Checking Docker images...
docker image inspect todo-backend:latest >nul 2>&1
if %errorlevel% neq 0 (
    echo    Warning: Backend image not found. Building...
    cd backend
    docker build -t todo-backend:latest .
    cd ..
) else (
    echo    OK: Backend image exists
)

docker image inspect todo-frontend:latest >nul 2>&1
if %errorlevel% neq 0 (
    echo    Warning: Frontend image not found. Building...
    cd frontend
    docker build -t todo-frontend:latest .
    cd ..
) else (
    echo    OK: Frontend image exists
)
echo.

REM Load images into Minikube
echo 3. Loading images into Minikube...
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
echo    OK: Images loaded into Minikube
echo.

REM Enable ingress addon
echo 4. Enabling NGINX Ingress Controller...
minikube addons list | findstr /C:"ingress: enabled" >nul
if %errorlevel% neq 0 (
    minikube addons enable ingress
    echo    OK: Ingress addon enabled
) else (
    echo    OK: Ingress addon already enabled
)
echo.

REM Deploy or upgrade Helm chart
echo 5. Deploying Helm chart...
helm list | findstr /C:"todo-chatbot" >nul
if %errorlevel% neq 0 (
    echo    Installing new release...
    helm install todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml
) else (
    echo    Upgrading existing release...
    helm upgrade todo-chatbot ./todo-chatbot -f ./todo-chatbot/values-local.yaml
)
echo    OK: Helm chart deployed
echo.

REM Wait for pods to be ready
echo 6. Waiting for pods to be ready...
kubectl wait --for=condition=ready pod -l app.kubernetes.io/instance=todo-chatbot --timeout=300s
echo    OK: All pods are ready
echo.

REM Get access information
echo =========================================
echo Deployment Complete!
echo =========================================
echo.

for /f "tokens=*" %%i in ('minikube ip') do set MINIKUBE_IP=%%i

echo Access your application:
echo.
echo 1. NodePort (Recommended):
echo    Frontend: http://%MINIKUBE_IP%:30080
echo.
echo 2. Ingress (Add to hosts file first):
echo    Add this line to C:\Windows\System32\drivers\etc\hosts:
echo    %MINIKUBE_IP% todo-app.local
echo    Then access: http://todo-app.local
echo.
echo 3. Port Forward:
echo    Run: kubectl port-forward svc/todo-chatbot-frontend 3000:3000
echo    Then access: http://localhost:3000
echo.
echo Useful commands:
echo   - View pods: kubectl get pods
echo   - View services: kubectl get svc
echo   - View logs (backend): kubectl logs -l app.kubernetes.io/component=backend -f
echo   - View logs (frontend): kubectl logs -l app.kubernetes.io/component=frontend -f
echo   - Uninstall: helm uninstall todo-chatbot
echo.

pause
