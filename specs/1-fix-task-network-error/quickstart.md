# Quickstart: Fix Network Error During Task Creation

## Overview
This guide explains how to implement the fix for the "Network error: Please check your connection" issue that occurs when creating tasks.

## Prerequisites
- Node.js and npm for frontend
- Python 3.12 and pip for backend
- Existing development environment with frontend and backend running

## Implementation Steps

### 1. Update API Client Token Handling
Modify `frontend/src/lib/api.ts` to enhance the `getAuthHeaders()` function:
- Check for tokens in localStorage first
- Fall back to NextAuth.js global state if not found
- Maintain synchronous function interface for backward compatibility

### 2. Verify API Configuration
Confirm that `NEXT_PUBLIC_API_URL` in `.env.local` matches the backend URL:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### 3. Test Authentication Flow
- Start both frontend and backend servers
- Log in to the application
- Attempt to create a task
- Verify the task is created without network errors

### 4. Error Handling Verification
- Test with invalid/expired tokens
- Confirm appropriate error messages are displayed
- Verify that authentication errors are distinguished from network errors

## Expected Results
- Task creation succeeds without "Network error: Please check your connection" messages
- Proper authentication tokens are included in all API requests
- Clear error messages for different failure scenarios
- Backward compatibility maintained with existing code

## Troubleshooting
- If network errors persist, check that both servers are running
- Verify that authentication is working by visiting protected routes
- Check browser console for specific error messages
- Confirm that CORS is properly configured on the backend