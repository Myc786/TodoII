# Frontend Deployment Guide - Vercel

## Prerequisites

1. Vercel account (https://vercel.com)
2. Backend deployed to Hugging Face Spaces
3. Node.js 18+ installed locally

## Step 1: Prepare Environment Variables

Before deploying, you need these values from your backend:

| Variable | Get From | Example |
|----------|----------|---------|
| `NEXT_PUBLIC_API_URL` | Backend URL + `/api` | `https://myc786-part2.hf.space/api` |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | Backend URL + `/api/auth` | `https://myc786-part2.hf.space/api/auth` |
| `NEXT_PUBLIC_BETTER_AUTH_SECRET` | Same as backend secret | Copy from HF Space secrets |
| `NEXT_PUBLIC_APP_NAME` | Your app name | `Todo App` |

## Step 2: Deploy to Vercel

### Option A: Using Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Navigate to frontend directory
cd frontend

# Deploy to production
vercel --prod
```

During deployment, you'll be asked:
- **Set up and deploy**: Yes
- **Which scope**: Select your account
- **Link to existing project**: If this is first deploy, select "No"
- **Project name**: `todo-app-frontend` (or your choice)
- **Directory**: `./` (current directory)
- **Override settings**: No

### Option B: Using Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your Git repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Install Command**: `npm install`
   - **Node Version**: 18.x

5. Add Environment Variables (see Step 3)
6. Click "Deploy"

### Option C: Connect Git Repository (Continuous Deployment)

1. Push your code to GitHub
2. Go to Vercel dashboard → Add New → Project
3. Select your repository
4. Vercel will auto-detect Next.js
5. Set Root Directory to `frontend`
6. Add environment variables
7. Deploy

Every push to your main branch will auto-deploy!

## Step 3: Configure Environment Variables in Vercel

### Via Dashboard

1. Go to your project settings
2. Click "Environment Variables"
3. Add each variable:

```
NEXT_PUBLIC_API_URL=https://myc786-part2.hf.space/api
NEXT_PUBLIC_BETTER_AUTH_URL=https://myc786-part2.hf.space/api/auth
NEXT_PUBLIC_BETTER_AUTH_SECRET=your_production_secret_key_min_32_chars
NEXT_PUBLIC_APP_NAME=Todo App
NEXT_PUBLIC_BASE_URL=https://your-app.vercel.app
```

4. Select environments: Production, Preview, Development
5. Click "Save"

### Via CLI

```bash
# Set variables for production
vercel env add NEXT_PUBLIC_API_URL production
# Enter: https://myc786-part2.hf.space/api

vercel env add NEXT_PUBLIC_BETTER_AUTH_URL production
# Enter: https://myc786-part2.hf.space/api/auth

vercel env add NEXT_PUBLIC_BETTER_AUTH_SECRET production
# Enter: your_secret_key

vercel env add NEXT_PUBLIC_APP_NAME production
# Enter: Todo App
```

## Step 4: Update Backend CORS

After deploying, you'll get a Vercel URL like:
```
https://your-app.vercel.app
```

Update your backend's `FRONTEND_URL` environment variable in HF Space:

1. Go to https://huggingface.co/spaces/myc786/Part2/settings
2. Find "Variables and secrets"
3. Update `FRONTEND_URL`:
   ```
   https://your-app.vercel.app
   ```
4. The Space will automatically restart

## Step 5: Verify Deployment

1. **Visit your Vercel URL**: https://your-app.vercel.app
2. **Test registration**:
   - Click "Sign Up"
   - Create an account
   - Should redirect to dashboard

3. **Test login**:
   - Log out
   - Log back in
   - Should work without errors

4. **Test task operations**:
   - Create a task
   - Complete a task
   - Edit a task
   - Delete a task

5. **Check browser console**:
   - Open DevTools (F12)
   - Look for errors
   - Should see successful API calls

## Troubleshooting

### CORS Errors

**Error**: "Access to fetch has been blocked by CORS policy"

**Fix**:
1. Check backend `FRONTEND_URL` includes your Vercel domain
2. Ensure backend is running on HF Spaces
3. Check browser console for exact origin error
4. Add domain to backend's allowed origins in `src/main.py`

### Authentication Errors

**Error**: "Invalid token" or "Unauthorized"

**Fix**:
1. Verify `NEXT_PUBLIC_BETTER_AUTH_SECRET` matches backend
2. Check backend health: https://myc786-part2.hf.space/health
3. Clear browser cache and cookies
4. Try incognito mode

### Network Errors

**Error**: "Failed to fetch" or "Network error"

**Fix**:
1. Check backend is running: https://myc786-part2.hf.space/health
2. Verify `NEXT_PUBLIC_API_URL` is correct (includes `/api`)
3. Check HF Space logs for backend errors
4. Test API directly with curl

### Build Failures

**Error**: Build fails on Vercel

**Fix**:
1. Check build logs in Vercel dashboard
2. Common issues:
   - Missing dependencies: `npm install` locally
   - TypeScript errors: `npm run build` locally
   - Environment variables: Check they're set in Vercel
3. Ensure `package.json` has correct scripts:
   ```json
   {
     "scripts": {
       "build": "next build",
       "start": "next start"
     }
   }
   ```

### Environment Variables Not Working

**Error**: Variables showing as `undefined`

**Fix**:
1. Verify variables start with `NEXT_PUBLIC_` (required for client-side)
2. Redeploy after adding variables
3. Check variables are set for "Production" environment
4. Clear Vercel cache: Settings → Data Cache → Purge

## Updating the Deployment

### With Git (Continuous Deployment)

```bash
git add .
git commit -m "Update: description"
git push origin main
```

Vercel will automatically deploy!

### With CLI

```bash
cd frontend
vercel --prod
```

### Manual

1. Go to Vercel dashboard
2. Click your project
3. Click "Deployments"
4. Click "..." on latest → "Redeploy"

## Custom Domain (Optional)

1. Go to project Settings → Domains
2. Add your domain: `yourdomain.com`
3. Add DNS records from Vercel to your domain provider
4. Wait for DNS propagation (5-30 minutes)
5. Update backend `FRONTEND_URL` to include new domain

## Monitoring

- **Vercel Dashboard**: https://vercel.com/dashboard
- **Analytics**: Enable in project settings
- **Logs**: View in project → Logs tab
- **Performance**: Vercel provides built-in analytics

## Rollback

If deployment fails, rollback to previous version:

1. Go to Deployments tab
2. Find last working deployment
3. Click "..." → "Promote to Production"

## Performance Optimization

### Enable Caching

In `next.config.js`:
```javascript
module.exports = {
  images: {
    unoptimized: false, // Enable image optimization
  },
  compress: true, // Enable gzip compression
}
```

### Use Environment Variables for API URLs

Never hardcode URLs. Always use environment variables.

### Enable Vercel Analytics

```bash
npm install @vercel/analytics
```

In `app/layout.tsx`:
```typescript
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

## Security Checklist

- [ ] All secrets in environment variables
- [ ] HTTPS enabled (automatic on Vercel)
- [ ] CORS configured correctly on backend
- [ ] No sensitive data in client code
- [ ] Authentication tokens stored securely
- [ ] Regular dependency updates

## Cost

- **Free tier**:
  - Unlimited deployments
  - 100 GB bandwidth/month
  - Hobby projects
- **Pro tier** ($20/month):
  - Team collaboration
  - Custom domains
  - Priority support

## Support

- Vercel Docs: https://vercel.com/docs
- Vercel Support: https://vercel.com/support
- Next.js Docs: https://nextjs.org/docs
- Community: https://github.com/vercel/next.js/discussions
