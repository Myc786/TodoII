# Technology Stack

**Analysis Date:** 2026-02-03

## Languages

**Primary:**
- Python 3.12.6 - Backend API and services (`backend/src/`)
- TypeScript 5.2.2 - Frontend application (`frontend/src/`)

**Secondary:**
- JavaScript - Frontend components and utilities
- SQL - Database queries and migrations

## Runtime

**Environment:**
- Python 3.12.6
- Node.js v22.12.0

**Package Manager:**
- pip - Python dependencies
- npm 10.9.2 - JavaScript/TypeScript dependencies
- Lockfile: requirements.txt (Python), package-lock.json (JavaScript)

## Frameworks

**Core:**
- FastAPI 0.115.0 - Backend web framework (`backend/src/`)
- Next.js 14.0.3 - Frontend framework (`frontend/src/`)
- React 18.2.0 - Frontend UI library

**Testing:**
- Not explicitly configured in package manifests

**Build/Dev:**
- Tailwind CSS - Styling framework
- Vite/Bundler - Part of Next.js ecosystem

## Key Dependencies

**Critical:**
- sqlmodel 0.0.22 - Database ORM with SQLAlchemy and Pydantic integration
- psycopg2-binary 2.9.9 - PostgreSQL database adapter
- python-jose[cryptography] 3.3.0 - JWT token handling
- uvicorn[standard] 0.36.0 - ASGI server
- openai 1.70.0 - OpenAI API integration

**Infrastructure:**
- alembic 1.14.0 - Database migration tool
- passlib[bcrypt] 1.7.4 - Password hashing
- @auth/core 0.20.0 - Authentication core library
- next-auth 4.24.5 - Next.js authentication library

## Configuration

**Environment:**
- Backend: `.env` file with DATABASE_URL, BETTER_AUTH_SECRET, etc.
- Frontend: `.env.local` with NEXT_PUBLIC_API_URL, NEXT_PUBLIC_BETTER_AUTH_URL, etc.
- Key configs required: Database URL, authentication secret, API endpoints

**Build:**
- Frontend: `tsconfig.json`, `tailwind.config.js`, `postcss.config.js`
- Backend: Standard Python packaging with `pyproject.toml`

## Platform Requirements

**Development:**
- Python 3.12+
- Node.js 18+
- SQLite (default) or PostgreSQL database

**Production:**
- Web server capable of running FastAPI (backend)
- Web server capable of serving Next.js application (frontend)
- Database (SQLite or PostgreSQL)

---

*Stack analysis: 2026-02-03*