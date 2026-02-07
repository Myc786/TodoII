# Deployment Information

## Deployment Status
✅ **Frontend**: Successfully Deployed to Vercel
✅ **Backend**: Configured for Hugging Face Spaces (Docker)
🔧 **Integration**: Ready for production deployment

**Quick Start**: See [QUICKSTART_GUIDE.md](QUICKSTART_GUIDE.md)

---

## Backend Deployment (Hugging Face Spaces)

### URLs
- **Space URL**: https://huggingface.co/spaces/myc786/Part2
- **API Base URL**: https://myc786-part2.hf.space
- **Health Check**: https://myc786-part2.hf.space/health

### Deployment Details
- **Platform**: Hugging Face Spaces
- **SDK**: Docker
- **Port**: 7860 (Hugging Face default)
- **Framework**: FastAPI with Uvicorn

### Files Deployed
- `Dockerfile` - Docker configuration for the backend
- `requirements.txt` - Python dependencies
- `src/` - Main application source code
- `README.md` - Space metadata and documentation

### Environment Variables (Set in HF Space Settings)
Configure these in your Hugging Face Space settings:
- `DATABASE_URL` - PostgreSQL connection string (e.g., from Neon or Supabase)
- `BETTER_AUTH_SECRET` - JWT secret key for authentication (min 32 chars)
- `ENVIRONMENT` - Set to `production`
- `FRONTEND_URL` - Your Vercel frontend URL for CORS
- `OPENAI_API_KEY` - (Optional) For AI chat features

**Generate secure secret**:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Frontend Deployment (Vercel)

### URLs
- **Main URL**: https://frontend-mocha-beta-73.vercel.app
- **Alternative URL**: https://frontend-qmwqrks1n-myc786s-projects.vercel.app

### Build Information
- **Framework**: Next.js 14.0.3
- **Build Time**: ~47 seconds
- **Build Location**: Washington, D.C., USA (East) – iad1
- **Build Status**: ✓ Compiled successfully

### Routes Generated
- `/` - Landing page (11.7 kB)
- `/dashboard` - Main dashboard (5.26 kB)
- `/login` - Login page (4.07 kB)
- `/signup` - Signup page (4.19 kB)
- `/forgot-password` - Password recovery (3.27 kB)
- `/reset-password` - Password reset (3.22 kB)

---

## Environment Variables

### Frontend (Vercel Environment Variables)
Set these in Vercel Dashboard → Project Settings → Environment Variables:
```env
NEXT_PUBLIC_API_URL=https://myc786-part2.hf.space/api
NEXT_PUBLIC_BETTER_AUTH_URL=https://myc786-part2.hf.space/api/auth
NEXT_PUBLIC_BETTER_AUTH_SECRET=same-as-backend-secret
NEXT_PUBLIC_APP_NAME=Todo App
NEXT_PUBLIC_BASE_URL=https://frontend-mocha-beta-73.vercel.app
```

**IMPORTANT**: BETTER_AUTH_SECRET must match the backend secret exactly!

### Backend (Hugging Face Space Secrets)
```env
DATABASE_URL=postgresql://user:password@host:5432/database
BETTER_AUTH_SECRET=your-production-secret-key
ENVIRONMENT=production
OPENAI_API_KEY=sk-your-openai-key (optional)
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/auth/signup` | POST | User registration |
| `/api/auth/login` | POST | User login |
| `/api/tasks` | GET | List tasks |
| `/api/tasks` | POST | Create task |
| `/api/tasks/{id}` | PUT | Update task |
| `/api/tasks/{id}` | DELETE | Delete task |
| `/api/tags` | GET | List tags |
| `/api/chat` | POST | Chat with AI assistant |

---

## Deployment Commands

### Redeploy Backend to Hugging Face
```bash
cd backend
python deploy_to_hf.py
```

### Redeploy Frontend to Vercel
```bash
cd frontend
vercel --prod
```

---

## Troubleshooting

### Backend Issues
1. Check Hugging Face Space logs: https://huggingface.co/spaces/myc786/Part2
2. Verify environment variables are set in Space settings
3. Check if the Docker build completed successfully
4. Ensure database connection string is correct

### Frontend Issues
1. Check Vercel deployment logs: https://vercel.com/myc786s-projects/frontend
2. Verify environment variables are set correctly in Vercel dashboard
3. Ensure backend API is accessible and CORS is configured properly
4. Check browser console for any client-side errors

### CORS Configuration
The backend is configured to allow all origins (`*`). For production, update `src/main.py` to specify allowed origins:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://frontend-mocha-beta-73.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         User Browser                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Vercel)                         │
│              https://frontend-mocha-beta-73.vercel.app       │
│                        Next.js 14                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Backend API (Hugging Face Spaces)               │
│                https://myc786-part2.hf.space                 │
│                    FastAPI + Uvicorn                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                       │
│                  (External Database Service)                 │
└─────────────────────────────────────────────────────────────┘
```
