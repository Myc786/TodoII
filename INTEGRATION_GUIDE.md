# Integration Guide: Frontend (Vercel) + Backend (Hugging Face Spaces)

This guide explains how to properly configure the integration between the deployed frontend on Vercel and backend on Hugging Face Spaces.

## Required Configuration

### Backend (Hugging Face Spaces) - Environment Variables

Configure these in your Hugging Face Space settings:

```
DATABASE_URL=postgresql://user:password@host:5432/database
BETTER_AUTH_SECRET=your-production-secret-key  # Must match between frontend and backend for any shared auth
ENVIRONMENT=production
OPENAI_API_KEY=sk-your-openai-key (optional)
```

### Frontend (Vercel) - Environment Variables

Configure these in your Vercel dashboard:

```
NEXT_PUBLIC_API_URL=https://myc786-part2.hf.space/api
NEXT_PUBLIC_BETTER_AUTH_URL=https://myc786-part2.hf.space/api/auth
NEXT_PUBLIC_BETTER_AUTH_SECRET=your-production-secret-key  # Must match backend secret
NEXT_PUBLIC_APP_NAME=Todo App
NEXT_PUBLIC_BASE_URL=https://frontend-mocha-beta-73.vercel.app
```

## Key Changes Made to Fix Integration Issues

### 1. Fixed Hardcoded API URLs in Frontend
- Updated `frontend/src/lib/chatbot-api.ts` to use environment variable instead of hardcoded `http://localhost:8000/api/chat`

### 2. Updated Backend CORS Configuration
- Modified `backend/src/main.py` to have environment-aware CORS settings:
  - Development: allows all origins (`*`)
  - Production: restricts to specific domains including Vercel frontend domains

### 3. Authentication Token Handling
- Verified that authentication system uses proper JWT tokens that are passed between frontend and backend
- Backend validates tokens using the same secret key used for signing

## Deployment Steps

1. Update the `BETTER_AUTH_SECRET` in Hugging Face Spaces to a strong, shared secret key
2. Update the `NEXT_PUBLIC_BETTER_AUTH_SECRET` in Vercel to the same value (though this isn't used directly by frontend, it may be referenced)
3. Ensure `NEXT_PUBLIC_API_URL` in Vercel points to the correct backend URL
4. Redeploy both applications

## Verification

After deployment:

1. Test that the frontend can access the backend health endpoint: `https://myc786-part2.hf.space/health`
2. Test user registration/login flow to ensure JWT tokens are properly exchanged
3. Test task creation to verify the core functionality works
4. Check browser developer tools for any CORS or network errors

## Troubleshooting

- If getting CORS errors: Verify the backend's CORS configuration includes your frontend domain
- If authentication fails: Ensure the JWT secret is identical between backend and frontend
- If API calls fail: Check that NEXT_PUBLIC_API_URL is correctly set to the backend domain
- If chat features fail: Verify that the chatbot API endpoint uses the correct domain