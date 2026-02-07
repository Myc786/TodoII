# Deployment Checklist

Use this checklist to ensure proper deployment of both frontend and backend.

## Pre-Deployment Checklist

### Database Setup
- [ ] Created PostgreSQL database (Neon/Supabase/other)
- [ ] Have connection string in format: `postgresql://user:pass@host:port/db?sslmode=require`
- [ ] Tested connection string locally
- [ ] Database is accessible from internet

### Accounts & Access
- [ ] Hugging Face account created
- [ ] Vercel account created
- [ ] Git repository accessible (if using git-based deployment)
- [ ] Have necessary API keys (if using OpenAI features)

### Security
- [ ] Generated secure BETTER_AUTH_SECRET (32+ chars)
- [ ] Secrets NOT committed to git
- [ ] .env files in .gitignore
- [ ] Different secrets for dev/prod environments

## Backend Deployment Checklist

### Pre-Deploy
- [ ] Reviewed `backend/DEPLOYMENT.md`
- [ ] All Python dependencies in `requirements.txt`
- [ ] Dockerfile is properly configured
- [ ] README.md has correct space metadata
- [ ] Removed Vercel-specific files (api/, vercel.json)
- [ ] Local tests passing

### HF Space Configuration
- [ ] Created Space: `myc786/Part2`
- [ ] Space SDK set to: Docker
- [ ] Space visibility set (Public/Private)

### Environment Variables (HF Secrets)
Set in Space Settings → Variables and Secrets:
- [ ] `DATABASE_URL` = `postgresql://...?sslmode=require`
- [ ] `BETTER_AUTH_SECRET` = (generated secret, 32+ chars)
- [ ] `ENVIRONMENT` = `production`
- [ ] `FRONTEND_URL` = `https://frontend-mocha-beta-73.vercel.app`
- [ ] `OPENAI_API_KEY` = (optional, if using AI features)

### Deploy
- [ ] Run `cd backend && python deploy_to_hf.py`
- [ ] Wait for build to complete (check Logs tab)
- [ ] Build succeeded without errors

### Post-Deploy Verification
- [ ] Health check works: `curl https://myc786-part2.hf.space/health`
- [ ] Returns: `{"status":"healthy","environment":"production"}`
- [ ] API docs accessible: https://myc786-part2.hf.space/docs
- [ ] No errors in Space logs
- [ ] Database connection successful

### Test Backend API
- [ ] User registration works
- [ ] User login returns JWT token
- [ ] Tasks can be created
- [ ] Tasks can be retrieved
- [ ] Tasks can be updated
- [ ] Tasks can be deleted
- [ ] CORS headers present

**Test commands in**: `INTEGRATION_TEST.md`

## Frontend Deployment Checklist

### Pre-Deploy
- [ ] Reviewed `frontend/DEPLOYMENT.md`
- [ ] Backend is deployed and healthy
- [ ] Have backend URL: `https://myc786-part2.hf.space`
- [ ] Have BETTER_AUTH_SECRET from backend
- [ ] Local build succeeds: `npm run build`
- [ ] No TypeScript errors
- [ ] No ESLint errors

### Vercel Configuration
- [ ] Vercel CLI installed: `npm install -g vercel`
- [ ] Logged in: `vercel login`
- [ ] Project linked or will create new

### Environment Variables (Vercel Dashboard)
Set in Project Settings → Environment Variables:
- [ ] `NEXT_PUBLIC_API_URL` = `https://myc786-part2.hf.space/api`
- [ ] `NEXT_PUBLIC_BETTER_AUTH_URL` = `https://myc786-part2.hf.space/api/auth`
- [ ] `NEXT_PUBLIC_BETTER_AUTH_SECRET` = (same as backend)
- [ ] `NEXT_PUBLIC_APP_NAME` = `Todo App`
- [ ] `NEXT_PUBLIC_BASE_URL` = (your Vercel URL after first deploy)

### Deploy
- [ ] Run `cd frontend && npm install`
- [ ] Run `npm run build` (local test)
- [ ] Run `vercel --prod`
- [ ] Wait for deployment
- [ ] Deployment succeeded

### Post-Deploy Verification
- [ ] Site is accessible: https://frontend-mocha-beta-73.vercel.app
- [ ] No 404 errors
- [ ] CSS loads properly
- [ ] Images load properly
- [ ] No console errors (F12)

### Test Frontend
- [ ] Home page loads
- [ ] Sign up page loads
- [ ] Login page loads
- [ ] Can register new user
- [ ] Registration redirects to dashboard
- [ ] Can login with credentials
- [ ] Dashboard loads tasks
- [ ] Can create task
- [ ] Can complete task
- [ ] Can edit task
- [ ] Can delete task
- [ ] Can logout
- [ ] Token persists on page refresh

## Integration Testing Checklist

### CORS Configuration
- [ ] Frontend domain in backend FRONTEND_URL
- [ ] CORS headers present in API responses
- [ ] No CORS errors in browser console
- [ ] Preflight OPTIONS requests succeed

### Authentication Flow
- [ ] Registration creates account in database
- [ ] Login returns valid JWT token
- [ ] Token stored properly (localStorage/cookies)
- [ ] Token sent in Authorization header
- [ ] Protected routes require authentication
- [ ] Invalid tokens rejected (401)
- [ ] Token refresh works (if implemented)

### API Integration
- [ ] All API calls reach backend
- [ ] Responses returned correctly
- [ ] Error messages displayed properly
- [ ] Loading states work
- [ ] Optimistic updates work
- [ ] Concurrent requests handled

### Performance
- [ ] Page load time < 3 seconds
- [ ] API response time < 1 second
- [ ] No memory leaks
- [ ] Images optimized
- [ ] Bundle size reasonable

### Security
- [ ] HTTPS enabled (both domains)
- [ ] Secrets not exposed in client code
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF protection (if needed)
- [ ] Rate limiting (if implemented)

## Post-Deployment Checklist

### Update Backend CORS
After first frontend deploy, if URL changed:
- [ ] Update backend `FRONTEND_URL` in HF Space
- [ ] Backend restarted/redeployed
- [ ] CORS working with new URL

### Documentation
- [ ] Update DEPLOYMENT_INFO.md with actual URLs
- [ ] Document any custom configuration
- [ ] Note any issues encountered
- [ ] Document workarounds used

### Monitoring Setup
- [ ] Set up error tracking (optional)
- [ ] Configure alerts (optional)
- [ ] Enable Vercel Analytics (optional)
- [ ] Monitor HF Space usage

### Communication
- [ ] Share deployment URLs with team
- [ ] Document deployment process
- [ ] Note any manual steps required
- [ ] Share credentials securely (if needed)

## Rollback Plan

If deployment fails:

### Backend Rollback
- [ ] Know how to revert HF Space to previous version
- [ ] Have backup of working code
- [ ] Can redeploy previous version quickly

### Frontend Rollback
- [ ] Can promote previous Vercel deployment
- [ ] Have backup of working code
- [ ] Can revert environment variables

## Success Criteria

Deployment is successful when:
- ✅ Backend health check returns 200 OK
- ✅ Frontend loads without errors
- ✅ Can register new account
- ✅ Can login with credentials
- ✅ Can create, read, update, delete tasks
- ✅ No CORS errors
- ✅ No authentication errors
- ✅ Performance acceptable
- ✅ Mobile responsive (if applicable)
- ✅ All critical features working

## Next Steps After Successful Deployment

- [ ] Monitor logs for errors
- [ ] Set up continuous deployment (git push = deploy)
- [ ] Add custom domain (optional)
- [ ] Set up database backups
- [ ] Configure monitoring/alerting
- [ ] Plan for scaling (if needed)
- [ ] Document maintenance procedures
- [ ] Schedule regular updates

## Common Issues Reference

See these guides for troubleshooting:
- `backend/DEPLOYMENT.md` - Backend-specific issues
- `frontend/DEPLOYMENT.md` - Frontend-specific issues
- `INTEGRATION_TEST.md` - Testing procedures
- `DEPLOYMENT_INFO.md` - Architecture overview

## Support Contacts

- HF Spaces: https://huggingface.co/docs/hub/spaces
- Vercel Support: https://vercel.com/support
- Database Provider: (your database provider's support)

---

**Last Updated**: 2026-02-05
**Deployment Architecture**: Frontend (Vercel) + Backend (HF Spaces) + Database (PostgreSQL)
