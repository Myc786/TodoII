# Technology Stack

**Analysis Date:** 2026-02-04

## Languages

**Primary:**
- Python 3.11 - Backend API and services (`backend/`)
- TypeScript 5.2 - Frontend application (`frontend/`)

**Secondary:**
- JavaScript - Frontend components and utilities
- SQL - Database queries and migrations

## Runtime

**Environment:**
- Python 3.11
- Node.js (version not specified in package.json, but Next.js 14 requires Node 18+)

**Package Manager:**
- Poetry - Backend dependency management (`backend/pyproject.toml`)
- npm - Frontend dependency management (`frontend/package.json`)
- Lockfile: `backend/poetry.lock` and `frontend/package-lock.json` present

## Frameworks

**Core:**
- FastAPI 0.115.0 - Backend web framework
- Next.js 14.0.3 - Frontend React framework
- React 18.2.0 - Frontend component library

**Testing:**
- pytest - Backend testing framework
- Jest - Frontend testing (via Next.js built-in)

**Build/Dev:**
- uvicorn - ASGI server for backend
- Next.js development server - Frontend dev server

## Key Dependencies

**Critical:**
- sqlmodel 0.0.22 - Backend ORM/database modeling
- psycopg2-binary 2.9.9 - PostgreSQL adapter
- @auth/core 0.20.0 - Authentication framework
- @modelcontextprotocol/sdk 1.0.0 - Model Context Protocol SDK
- openai 1.70.0 (backend) and openai 4.0.0 (frontend) - OpenAI API clients

**Infrastructure:**
- python-jose[cryptography] 3.3.0 - JWT token handling
- alembic 1.14.0 - Database migration tool
- passlib[bcrypt] 1.7.4 - Password hashing
- tailwindcss - CSS styling framework

## Configuration

**Environment:**
- Backend: `.env` file with DATABASE_URL, BETTER_AUTH_SECRET, etc.
- Frontend: `.env.local` with NEXT_PUBLIC_API_URL, NEXT_PUBLIC_BETTER_AUTH_URL, etc.
- Key configs required: API URLs, authentication secrets, database connections

**Build:**
- Backend: `pyproject.toml` with poetry configuration
- Frontend: `next.config.js` (not visible but implied by package.json)

## Platform Requirements

**Development:**
- Python 3.11+
- Node.js 18+
- Poetry for backend dependency management
- npm/yarn for frontend dependency management

**Production:**
- Backend: ASGI-compatible server (uvicorn)
- Frontend: Static hosting or Node.js server for SSR
- Database: PostgreSQL (primary) or SQLite (development)

---

*Stack analysis: 2026-02-04*