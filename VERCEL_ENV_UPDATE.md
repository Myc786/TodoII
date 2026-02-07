# Update Vercel Environment Variables

## Backend Secrets Configured Successfully! ✅

Your backend is now configured with:
- ✅ PostgreSQL Database (Neon)
- ✅ Secure Authentication Secret
- ✅ Production Environment
- ✅ CORS for Frontend

**Backend Status**: 🟢 PRODUCTION MODE

---

## ⚠️ IMPORTANT: Update Frontend Environment Variables

Your frontend needs to use the **same** `BETTER_AUTH_SECRET` as the backend.

### Generated Secret (Use This):
```
ghLw-JPwjxA6ed4YsWa5QxB3atOZsA0CZnKK6rgQ_xs
```

---

## Method 1: Update via Vercel Dashboard (Recommended)

### Step-by-Step Instructions:

1. **Go to Vercel Dashboard**:
   ```
   https://vercel.com/myc786s-projects/frontend/settings/environment-variables
   ```

2. **Find `NEXT_PUBLIC_BETTER_AUTH_SECRET`**:
   - Look for this variable in the list
   - Click the "Edit" button (pencil icon)

3. **Update the Value**:
   - Replace the current value with:
     ```
     ghLw-JPwjxA6ed4YsWa5QxB3atOZsA0CZnKK6rgQ_xs
     ```
   - Click "Save"

4. **Verify Other Variables**:
   Make sure these are also set correctly:

   | Variable | Value |
   |----------|-------|
   | `NEXT_PUBLIC_API_URL` | `https://myc786-part2.hf.space/api` |
   | `NEXT_PUBLIC_BETTER_AUTH_URL` | `https://myc786-part2.hf.space/api/auth` |
   | `NEXT_PUBLIC_BETTER_AUTH_SECRET` | `ghLw-JPwjxA6ed4YsWa5QxB3atOZsA0CZnKK6rgQ_xs` |
   | `NEXT_PUBLIC_APP_NAME` | `Todo App` |

5. **Redeploy Frontend**:
   After updating variables, redeploy:
   - Go to "Deployments" tab
   - Click the "..." menu on latest deployment
   - Click "Redeploy"

   OR run:
   ```bash
   cd frontend
   vercel --prod
   ```

---

## Method 2: Update via Vercel CLI (Alternative)

```bash
cd frontend

# Remove old secret
vercel env rm NEXT_PUBLIC_BETTER_AUTH_SECRET production

# Add new secret
vercel env add NEXT_PUBLIC_BETTER_AUTH_SECRET production
# When prompted, enter: ghLw-JPwjxA6ed4YsWa5QxB3atOZsA0CZnKK6rgQ_xs

# Redeploy
vercel --prod
```

---

## Verification After Update

### 1. Test Backend Health (Should Work Now)
```bash
curl https://myc786-part2.hf.space/health
```

**Expected**:
```json
{
  "status": "healthy",
  "environment": "production"
}
```

### 2. Test Frontend (After Redeploy)
Visit: https://frontend-mocha-beta-73.vercel.app

**Should see**:
- No console errors (F12)
- Pages load correctly
- Ready to sign up/login

### 3. Test Full Integration

#### Register a User:
```bash
curl -X POST https://myc786-part2.hf.space/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "name": "Test User",
    "password": "SecurePass123!"
  }'
```

**Expected**: User created successfully

#### Login:
```bash
curl -X POST https://myc786-part2.hf.space/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "SecurePass123!"
  }'
```

**Expected**: JWT token returned

---

## Summary of Changes

### Backend (Hugging Face Spaces) ✅ COMPLETED
- ✅ `DATABASE_URL`: Neon PostgreSQL configured
- ✅ `BETTER_AUTH_SECRET`: `ghLw-JPwjxA6ed4YsWa5QxB3atOZsA0CZnKK6rgQ_xs`
- ✅ `ENVIRONMENT`: `production`
- ✅ `FRONTEND_URL`: `https://frontend-mocha-beta-73.vercel.app`
- ✅ Status: **RUNNING IN PRODUCTION MODE**

### Frontend (Vercel) ⏳ ACTION REQUIRED
- ⏳ Update `NEXT_PUBLIC_BETTER_AUTH_SECRET` to match backend
- ⏳ Redeploy after updating
- ⏳ Test registration and login

---

## Quick Check Commands

```bash
# Backend health (should show production)
curl https://myc786-part2.hf.space/health

# Frontend accessibility
curl -I https://frontend-mocha-beta-73.vercel.app

# Test CORS
curl -X OPTIONS https://myc786-part2.hf.space/api/tasks/ \
  -H "Origin: https://frontend-mocha-beta-73.vercel.app" \
  -H "Access-Control-Request-Method: GET" -I
```

---

## Troubleshooting

### Issue: "Invalid token" after login

**Cause**: Frontend and backend have different `BETTER_AUTH_SECRET`

**Fix**: Ensure both use: `ghLw-JPwjxA6ed4YsWa5QxB3atOZsA0CZnKK6rgQ_xs`

### Issue: Database connection errors

**Cause**: PostgreSQL credentials incorrect

**Solution**:
1. Test connection locally:
   ```bash
   psql 'postgresql://neondb_owner:npg_NvRFm7In8Xxk@ep-ancient-pine-aiy0po7g-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require'
   ```
2. If fails, regenerate credentials in Neon dashboard

### Issue: CORS errors

**Cause**: FRONTEND_URL doesn't match Vercel domain

**Current Config**: `https://frontend-mocha-beta-73.vercel.app` ✅

**Verify**: Check browser console for exact error

---

## Next Steps

1. [ ] Update `NEXT_PUBLIC_BETTER_AUTH_SECRET` in Vercel
2. [ ] Redeploy frontend
3. [ ] Test registration via frontend UI
4. [ ] Test login via frontend UI
5. [ ] Create and manage tasks
6. [ ] 🎉 Celebrate - your app is fully deployed!

---

**Need Help?**
- HF Space Logs: https://huggingface.co/spaces/myc786/Part2
- Vercel Logs: https://vercel.com/myc786s-projects/frontend
- Backend Health: https://myc786-part2.hf.space/health
- Frontend: https://frontend-mocha-beta-73.vercel.app
