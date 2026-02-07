# Backend Deployment Guide - Hugging Face Spaces

## Prerequisites

1. Hugging Face account (https://huggingface.co)
2. PostgreSQL database (recommended providers):
   - Neon (https://neon.tech) - Free tier available
   - Supabase (https://supabase.com) - Free tier available
   - ElephantSQL (https://www.elephantsql.com) - Free tier available

## Step 1: Create PostgreSQL Database

### Using Neon (Recommended)

1. Go to https://neon.tech and sign up
2. Create a new project
3. Copy the connection string (looks like):
   ```
   postgresql://username:password@hostname.neon.tech/dbname?sslmode=require
   ```

### Using Supabase

1. Go to https://supabase.com and sign up
2. Create a new project
3. Go to Settings → Database → Connection String
4. Copy the connection string

## Step 2: Create Hugging Face Space

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Configure:
   - **Owner**: Your username (e.g., myc786)
   - **Space name**: `Part2` or `todo-backend`
   - **License**: MIT
   - **Select the Space SDK**: Docker
   - **Space hardware**: CPU basic (free tier)
   - **Visibility**: Public or Private

## Step 3: Configure Secrets in HF Space

After creating the space, go to Settings → Variables and Secrets and add:

| Variable Name | Example Value | Required |
|--------------|---------------|----------|
| `DATABASE_URL` | `postgresql://user:pass@host:5432/db` | Yes |
| `BETTER_AUTH_SECRET` | `your-secure-random-32-char-string` | Yes |
| `ENVIRONMENT` | `production` | Yes |
| `FRONTEND_URL` | `https://frontend-mocha-beta-73.vercel.app` | Yes |
| `OPENAI_API_KEY` | `sk-your-openai-key` | No (for AI features) |

**To generate a secure secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Step 4: Deploy to Hugging Face

### Option A: Using the Deployment Script (Recommended)

```bash
cd backend
python deploy_to_hf.py
```

This will:
- Validate required files
- Push code to your HF Space
- Trigger automatic rebuild

### Option B: Manual Git Deployment

```bash
# Clone your HF Space repository
git clone https://huggingface.co/spaces/myc786/Part2
cd Part2

# Copy backend files
cp -r ../backend/* .

# Commit and push
git add .
git commit -m "Deploy backend"
git push
```

### Option C: Using HF Hub CLI

```bash
# Install huggingface_hub
pip install huggingface_hub

# Login
huggingface-cli login

# Upload files
cd backend
huggingface-cli upload myc786/Part2 . --repo-type space
```

## Step 5: Verify Deployment

1. Wait for the Space to build (check the Logs tab)
2. Once running, test the health endpoint:
   ```bash
   curl https://myc786-part2.hf.space/health
   ```

   Expected response:
   ```json
   {"status": "healthy", "environment": "production"}
   ```

3. Test API endpoints:
   ```bash
   # Register a user
   curl -X POST https://myc786-part2.hf.space/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "name": "Test User", "password": "securepass123"}'

   # Login
   curl -X POST https://myc786-part2.hf.space/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "password": "securepass123"}'
   ```

## Step 6: Update Frontend Configuration

In your Vercel project, set these environment variables:

```env
NEXT_PUBLIC_API_URL=https://myc786-part2.hf.space/api
NEXT_PUBLIC_BETTER_AUTH_URL=https://myc786-part2.hf.space/api/auth
NEXT_PUBLIC_BETTER_AUTH_SECRET=same-as-backend-secret
NEXT_PUBLIC_APP_NAME=Todo App
```

## Troubleshooting

### Build Failures

1. **Check logs** in the HF Space Logs tab
2. **Common issues**:
   - Missing dependencies in requirements.txt
   - Syntax errors in Python code
   - Docker build failures

### Database Connection Errors

1. **Verify connection string** format:
   ```
   postgresql://username:password@hostname:port/database
   ```
2. **Check SSL mode**: Add `?sslmode=require` for most cloud databases
3. **Test connection** locally:
   ```bash
   python -c "from sqlalchemy import create_engine; engine = create_engine('YOUR_CONNECTION_STRING'); conn = engine.connect(); print('Connected!')"
   ```

### CORS Errors

1. **Check FRONTEND_URL** environment variable matches your Vercel domain
2. **Update** src/main.py if you need to add more origins
3. **Verify** browser console for actual error

### Application Not Starting

1. **Check port**: HF Spaces expect port 7860
2. **Verify Dockerfile** CMD: `uvicorn src.main:app --host 0.0.0.0 --port 7860`
3. **Check logs** for startup errors

## Monitoring

- **HF Space Dashboard**: https://huggingface.co/spaces/myc786/Part2
- **API Health**: https://myc786-part2.hf.space/health
- **API Docs**: https://myc786-part2.hf.space/docs

## Updating the Deployment

```bash
cd backend
python deploy_to_hf.py
```

Or manually:
```bash
cd /path/to/hf-space-repo
git pull
# Make changes
git add .
git commit -m "Update: description"
git push
```

## Rollback

If deployment fails, HF keeps previous versions. To rollback:
1. Go to your Space settings
2. Find the Files tab
3. Revert to previous commit

## Security Checklist

- [ ] DATABASE_URL is set in HF Secrets (not in code)
- [ ] BETTER_AUTH_SECRET is strong and unique
- [ ] ENVIRONMENT is set to "production"
- [ ] CORS is configured for specific domains only
- [ ] PostgreSQL uses SSL connection
- [ ] No sensitive data in public files
- [ ] .env files are in .gitignore

## Cost Optimization

- **Free tier**: CPU basic (sufficient for most apps)
- **Database**: Use free tier from Neon or Supabase
- **Upgrade**: If you need more resources, upgrade Space hardware in settings

## Support

- HF Spaces Docs: https://huggingface.co/docs/hub/spaces
- Community: https://discuss.huggingface.co
- Issues: https://github.com/yourusername/project/issues
