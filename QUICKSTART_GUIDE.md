# Todo App - Quick Start Guide

Get your app deployed in 10 minutes!

## Prerequisites

- [ ] Hugging Face account
- [ ] Vercel account
- [ ] PostgreSQL database (Neon or Supabase)
- [ ] Node.js 18+ installed
- [ ] Python 3.11+ installed

## Step 1: Set Up Database (2 minutes)

### Option A: Neon (Recommended)

1. Visit https://neon.tech
2. Sign up and create project
3. Copy connection string
   ```
   postgresql://user:pass@host.neon.tech/db?sslmode=require
   ```

### Option B: Supabase

1. Visit https://supabase.com
2. Sign up and create project
3. Go to Settings → Database
4. Copy connection string

## Step 2: Deploy Backend (3 minutes)

1. **Configure HF Space Secrets**:
   - Go to https://huggingface.co/spaces/myc786/Part2/settings
   - Add these secrets:
     ```
     DATABASE_URL=postgresql://...  (from Step 1)
     BETTER_AUTH_SECRET=<generate-with-command-below>
     ENVIRONMENT=production
     FRONTEND_URL=https://frontend-mocha-beta-73.vercel.app
     ```

2. **Generate secure secret**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **Deploy**:
   ```bash
   cd backend
   python deploy_to_hf.py
   ```

4. **Verify**: Visit https://myc786-part2.hf.space/health
   - Should return: `{"status":"healthy","environment":"production"}`

## Step 3: Deploy Frontend (3 minutes)

1. **Set Vercel Environment Variables**:
   - Go to Vercel project settings
   - Add variables:
     ```
     NEXT_PUBLIC_API_URL=https://myc786-part2.hf.space/api
     NEXT_PUBLIC_BETTER_AUTH_URL=https://myc786-part2.hf.space/api/auth
     NEXT_PUBLIC_BETTER_AUTH_SECRET=<same-as-backend>
     NEXT_PUBLIC_APP_NAME=Todo App
     ```

2. **Deploy**:
   ```bash
   cd frontend
   npm install
   vercel --prod
   ```

3. **Verify**: Visit your Vercel URL

## Step 4: Test Integration (2 minutes)

1. **Backend health check**:
   ```bash
   curl https://myc786-part2.hf.space/health
   ```

2. **Frontend test**:
   - Visit https://frontend-mocha-beta-73.vercel.app
   - Sign up with test account
   - Create a task
   - Complete the task

## Troubleshooting

### Backend Issues

**Health check fails**
- Check HF Space logs
- Verify DATABASE_URL is correct
- Ensure all secrets are set

**Database connection error**
- Test connection string locally
- Add `?sslmode=require` to PostgreSQL URL
- Check database is accessible

### Frontend Issues

**CORS error**
- Verify FRONTEND_URL in backend matches Vercel domain
- Check backend CORS configuration
- Clear browser cache

**Auth error**
- Ensure BETTER_AUTH_SECRET matches backend
- Check backend is running
- Try incognito mode

**API not reachable**
- Verify NEXT_PUBLIC_API_URL is correct
- Check backend health endpoint
- Inspect network tab in browser

## Architecture

```
User Browser
    ↓
Frontend (Vercel)
https://frontend-mocha-beta-73.vercel.app
    ↓
Backend (HF Spaces)
https://myc786-part2.hf.space
    ↓
PostgreSQL Database
(Neon/Supabase)
```

## Support

- Backend Deployment Guide: `backend/DEPLOYMENT.md`
- Frontend Deployment Guide: `frontend/DEPLOYMENT.md`
- Integration Testing: `INTEGRATION_TEST.md`
