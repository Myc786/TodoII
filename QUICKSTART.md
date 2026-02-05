# Quickstart Guide: Vercel-HF Integration

## Prerequisites

- Access to Vercel dashboard for frontend deployment
- Access to Hugging Face Spaces for backend deployment
- Environment variables properly configured for both platforms

## Environment Configuration

### Backend (Hugging Face Spaces)

Required environment variables to set in Space settings:

```
DATABASE_URL=postgresql://user:password@host:5432/database
BETTER_AUTH_SECRET=your-production-secret-key  # Critical: must be strong and consistent
ENVIRONMENT=production
OPENAI_API_KEY=sk-your-openai-key (optional)
```

### Frontend (Vercel)

Required environment variables to set in Vercel dashboard:

```
NEXT_PUBLIC_API_URL=https://myc786-part2.hf.space/api
NEXT_PUBLIC_BETTER_AUTH_URL=https://myc786-part2.hf.space/api/auth
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-production-secret-key  # Must match backend secret
NEXT_PUBLIC_APP_NAME=Todo App
NEXT_PUBLIC_BASE_URL=https://frontend-mocha-beta-73.vercel.app
```

## Step-by-Step Setup

### 1. Configure Backend Environment
```bash
# Log into Hugging Face Hub
huggingface-cli login

# Set environment variables in your Space settings
# Access via: https://huggingface.co/spaces/myc786/Part2/settings
```

### 2. Update Frontend Configuration
```bash
# Access Vercel dashboard
# Go to: https://vercel.com/myc786s-projects/frontend/settings/environment-variables

# Add/update the environment variables listed above
```

### 3. Deploy Backend Changes
```bash
# Navigate to backend directory
cd backend

# Redeploy the space (make sure Dockerfile and requirements.txt are updated)
# Through Hugging Face UI or CLI
```

### 4. Deploy Frontend Changes
```bash
# Navigate to frontend directory
cd frontend

# Rebuild and deploy
npm run build
# Or redeploy through Vercel dashboard
```

## Verification Steps

### 1. Test Backend Health
```bash
curl https://myc786-part2.hf.space/health
# Expected response: {"status":"healthy","environment":"production"}
```

### 2. Test Frontend-Backend Connection
Open the frontend in a browser and check:
- Network tab for any CORS errors
- Authentication flow works
- Task creation functionality

### 3. Test Authentication Flow
1. Navigate to signup/login page
2. Create a new account or log in
3. Verify authentication token is received and stored
4. Test protected API endpoints

### 4. Test Core Functionality
1. Create a new task
2. Verify it appears in the task list
3. Toggle completion status
4. Edit and update a task
5. Delete a task

## Common Issues and Solutions

### CORS Errors
**Issue**: Requests blocked due to CORS policy
**Solution**: Ensure backend has the correct frontend domain in the CORS configuration

### Authentication Failures
**Issue**: Unable to log in or token validation fails
**Solution**: Verify that JWT secrets match between frontend and backend

### API Call Failures
**Issue**: Network errors when making API calls
**Solution**: Check that NEXT_PUBLIC_API_URL points to the correct backend URL

### SSL/TLS Issues
**Issue**: Mixed content warnings or HTTPS errors
**Solution**: Ensure all connections use HTTPS, especially in production

## Monitoring and Debugging

### Frontend Debugging
- Check browser console for JavaScript errors
- Monitor Network tab for failed API requests
- Inspect localStorage for authentication tokens

### Backend Debugging
- Check Hugging Face Space logs for errors
- Verify environment variables are correctly set
- Test API endpoints directly using curl or Postman

## Next Steps

Once integration is verified:
1. Monitor application performance
2. Set up proper logging and error tracking
3. Implement proper error handling for network failures
4. Add loading states and error boundaries for better UX