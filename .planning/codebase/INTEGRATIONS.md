# External Integrations

**Analysis Date:** 2026-02-03

## APIs & External Services

**AI/ML Services:**
- OpenAI API - Used for chatbot functionality
  - SDK/Client: openai package (versions 1.70.0 backend, 4.0.0 frontend)
  - Auth: NEXT_PUBLIC_OPENAI_API_KEY (inferred from usage)

## Data Storage

**Databases:**
- SQLite/PostgreSQL - Main application database
  - Connection: DATABASE_URL environment variable
  - Client: sqlmodel with psycopg2-binary for PostgreSQL

**File Storage:**
- Local filesystem only

**Caching:**
- None explicitly configured

## Authentication & Identity

**Auth Provider:**
- Custom JWT-based authentication
  - Implementation: Custom JWT token generation with python-jose, argon2/bcrypt password hashing

## Monitoring & Observability

**Error Tracking:**
- None explicitly configured

**Logs:**
- Standard Python logging with configurable LOG_LEVEL environment variable

## CI/CD & Deployment

**Hosting:**
- Not explicitly configured in manifests (likely cloud platform agnostic)

**CI Pipeline:**
- None explicitly configured in manifests

## Environment Configuration

**Required env vars:**
- BACKEND: DATABASE_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL, ENVIRONMENT, LOG_LEVEL
- FRONTEND: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_BETTER_AUTH_URL, NEXT_PUBLIC_BETTER_AUTH_SECRET, NEXT_PUBLIC_BASE_URL

**Secrets location:**
- .env files for backend, .env.local for frontend

## Webhooks & Callbacks

**Incoming:**
- None explicitly configured

**Outgoing:**
- OpenAI API calls for chatbot functionality
- Potential webhook endpoints for external services (not explicitly configured)

---

*Integration audit: 2026-02-03*