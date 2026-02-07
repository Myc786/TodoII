#!/bin/bash

# Deployment script for Todo App
# Deploys backend to Hugging Face Spaces and frontend to Vercel

set -e  # Exit on error

echo "========================================="
echo "Todo App Deployment Script"
echo "========================================="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if in correct directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo -e "${RED}Error: Must run from project root directory${NC}"
    exit 1
fi

# Function to deploy backend
deploy_backend() {
    echo -e "\n${YELLOW}=== Deploying Backend to Hugging Face ===${NC}"
    cd backend

    # Check if required files exist
    if [ ! -f "Dockerfile" ]; then
        echo -e "${RED}Error: Dockerfile not found${NC}"
        exit 1
    fi

    if [ ! -f "requirements.txt" ]; then
        echo -e "${RED}Error: requirements.txt not found${NC}"
        exit 1
    fi

    # Run deployment script
    if [ -f "deploy_to_hf.py" ]; then
        echo "Running HF deployment script..."
        python deploy_to_hf.py

        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Backend deployed successfully to Hugging Face${NC}"
            echo "Backend URL: https://myc786-part2.hf.space"
        else
            echo -e "${RED}✗ Backend deployment failed${NC}"
            exit 1
        fi
    else
        echo -e "${YELLOW}Manual deployment required:${NC}"
        echo "1. Go to https://huggingface.co/spaces/myc786/Part2"
        echo "2. Upload files via web interface or git push"
        echo "3. Check build logs"
    fi

    cd ..
}

# Function to deploy frontend
deploy_frontend() {
    echo -e "\n${YELLOW}=== Deploying Frontend to Vercel ===${NC}"
    cd frontend

    # Check if Vercel CLI is installed
    if ! command -v vercel &> /dev/null; then
        echo -e "${YELLOW}Vercel CLI not found. Installing...${NC}"
        npm install -g vercel
    fi

    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "Installing dependencies..."
        npm install
    fi

    # Build locally to check for errors
    echo "Building frontend..."
    npm run build

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Build successful${NC}"
    else
        echo -e "${RED}✗ Build failed. Fix errors before deploying.${NC}"
        exit 1
    fi

    # Deploy to Vercel
    echo "Deploying to Vercel..."
    vercel --prod --yes

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Frontend deployed successfully to Vercel${NC}"
    else
        echo -e "${RED}✗ Frontend deployment failed${NC}"
        exit 1
    fi

    cd ..
}

# Function to test integration
test_integration() {
    echo -e "\n${YELLOW}=== Testing Integration ===${NC}"

    # Test backend health
    echo "Testing backend health..."
    HEALTH_STATUS=$(curl -s https://myc786-part2.hf.space/health | jq -r .status 2>/dev/null)

    if [ "$HEALTH_STATUS" = "healthy" ]; then
        echo -e "${GREEN}✓ Backend is healthy${NC}"
    else
        echo -e "${RED}✗ Backend health check failed${NC}"
        echo "Check https://huggingface.co/spaces/myc786/Part2 for logs"
    fi

    # Test frontend
    echo "Testing frontend..."
    FRONTEND_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://frontend-mocha-beta-73.vercel.app)

    if [ "$FRONTEND_STATUS" = "200" ]; then
        echo -e "${GREEN}✓ Frontend is accessible${NC}"
    else
        echo -e "${RED}✗ Frontend check failed (Status: $FRONTEND_STATUS)${NC}"
    fi
}

# Main deployment flow
main() {
    echo "What would you like to deploy?"
    echo "1) Backend only"
    echo "2) Frontend only"
    echo "3) Both (backend first, then frontend)"
    echo "4) Test integration only"
    read -p "Enter choice (1-4): " choice

    case $choice in
        1)
            deploy_backend
            ;;
        2)
            deploy_frontend
            ;;
        3)
            deploy_backend
            deploy_frontend
            test_integration
            ;;
        4)
            test_integration
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            exit 1
            ;;
    esac

    echo -e "\n${GREEN}========================================="
    echo "Deployment Complete!"
    echo "=========================================${NC}"
    echo ""
    echo "Backend: https://myc786-part2.hf.space"
    echo "Frontend: https://frontend-mocha-beta-73.vercel.app"
    echo ""
    echo "Next steps:"
    echo "1. Verify environment variables in HF Space settings"
    echo "2. Verify environment variables in Vercel dashboard"
    echo "3. Test authentication flow on frontend"
    echo "4. Check logs for any errors"
}

# Run main function
main
