# External Integrations

**Analysis Date:** 2026-02-04

## APIs & External Services

**AI/ML:**
- OpenAI - AI-powered features and chatbot functionality
  - SDK/Client: openai package (1.70.0 backend, 4.0.0 frontend)
  - Auth: OPENAI_API_KEY environment variable (likely)

**Authentication:**
- Better Auth / @auth/core - Authentication framework
  - SDK/Client: @auth/core 0.20.0, next-auth 4.24.5
  - Auth: NEXT_PUBLIC_BETTER_AUTH_SECRET environment variable

## Data Storage

**Databases:**
- PostgreSQL 2.9.9 - Primary database client
  - Connection: DATABASE_URL environment variable
  - Client: psycopg2-binary with sqlmodel ORM
- SQLite - Development/testing database
  - Connection: DATABASE_URL="sqlite:///./todo_app.db"

## Authentication & Identity

**Auth Provider:**
- Custom JWT-based authentication
  - Implementation: python-jose for token handling, custom auth routes in FastAPI
  - Token expiration: 30 minutes (ACCESS_TOKEN_EXPIRE_MINUTES)

## Monitoring & Observability

**Error Tracking:**
- None explicitly configured (no Sentry, Bugsnag, etc. detected)

**Logs:**
- Standard logging via Python logging module
- Console output for development

## CI/CD & Deployment

**Hosting:**
- Not explicitly configured (no Vercel, AWS, etc. detected in config)

**CI Pipeline:**
- None detected in repository (no GitHub Actions, CircleCI config files)

## Environment Configuration

**Required env vars:**
- Backend: DATABASE_URL, BETTER_AUTH_SECRET, ENVIRONMENT, LOG_LEVEL
- Frontend: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_BETTER_AUTH_URL, NEXT_PUBLIC_BETTER_AUTH_SECRET

**Secrets location:**
- .env files for backend and .env.local for frontend

## Webhooks & Callbacks

**Incoming:**
- None detected in codebase

**Outgoing:**
- OpenAI API calls for AI features
- Potential webhook endpoints not explicitly defined in current codebase

---

*Integration audit: 2026-02-04*