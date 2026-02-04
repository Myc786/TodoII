# Codebase Structure

**Analysis Date:** 2026-02-04

## Directory Layout

```
D:\part2\
├── backend/          # Backend API server with FastAPI
│   ├── migrations/   # Database migration files
│   └── src/          # Backend source code
│       ├── api/      # API routes and dependencies
│       ├── core/     # Core utilities and configuration
│       ├── database/ # Database connection and initialization
│       ├── mcp_tools/# MCP tools and utilities
│       ├── models/   # Data models and schemas
│       └── services/ # Business logic services
├── frontend/         # Frontend Next.js application
│   ├── src/          # Frontend source code
│   │   ├── app/      # Next.js app directory with pages
│   │   ├── components/ # Reusable UI components
│   │   ├── contexts/ # React context providers
│   │   ├── hooks/    # Custom React hooks
│   │   └── lib/      # Shared libraries and utilities
│   └── public/       # Static assets
├── .planning/        # Planning and analysis documents
│   └── codebase/     # Codebase analysis documents
├── .specify/         # Specification tools and templates
└── specs/            # Feature specifications
```

## Directory Purposes

**backend/:**
- Purpose: Contains the FastAPI backend server
- Contains: API routes, models, services, database setup
- Key files: `D:\part2\backend\src\main.py`, `D:\part2\backend\requirements.txt`

**frontend/:**
- Purpose: Contains the Next.js frontend application
- Contains: Pages, components, hooks, API utilities
- Key files: `D:\part2\frontend\src\app\layout.tsx`, `D:\part2\frontend\package.json`

**backend/src/api/:**
- Purpose: API route definitions and dependencies
- Contains: FastAPI routers, authentication deps
- Key files: `D:\part2\backend\src\api\routes\tasks.py`, `D:\part2\backend\src\api\deps.py`

**backend/src/models/:**
- Purpose: Data models and Pydantic schemas
- Contains: SQLModel definitions, enums
- Key files: `D:\part2\backend\src\models\task.py`, `D:\part2\backend\src\models\task_schemas.py`

**backend/src/services/:**
- Purpose: Business logic implementations
- Contains: Service classes with CRUD operations
- Key files: `D:\part2\backend\src\services\task_service.py`

**frontend/src/components/:**
- Purpose: Reusable UI components
- Contains: Task components, UI primitives, auth components
- Key files: `D:\part2\frontend\src\components\task\task-list.tsx`

## Key File Locations

**Entry Points:**
- `D:\part2\backend\src\main.py`: Backend FastAPI application
- `D:\part2\frontend\src\app\layout.tsx`: Frontend Next.js root layout

**Configuration:**
- `D:\part2\backend\src\core\config.py`: Backend configuration
- `D:\part2\frontend\src\contexts\theme-context.tsx`: Frontend theme configuration

**Core Logic:**
- `D:\part2\backend\src\services\task_service.py`: Task business logic
- `D:\part2\frontend\src\lib\api.ts`: Frontend API utilities

**Testing:**
- `D:\part2\backend\test_crud_endpoints.py`: Backend tests

## Naming Conventions

**Files:**
- Backend: snake_case (e.g., `task_service.py`)
- Frontend: kebab-case or camelCase (e.g., `task-list.tsx`)

**Functions:**
- Backend: snake_case (e.g., `get_tasks_by_user_id`)
- Frontend: camelCase (e.g., `handleSearch`)

## Where to Add New Code

**New Feature:**
- Primary code: `D:\part2\backend\src\services\` and `D:\part2\frontend\src\components\`
- Tests: `D:\part2\backend\tests\` and alongside component files

**New API Endpoint:**
- Implementation: `D:\part2\backend\src\api\routes\`
- Frontend integration: `D:\part2\frontend\src\lib\api.ts`

**New Component:**
- Implementation: `D:\part2\frontend\src\components\`
- Integration: In appropriate page files under `D:\part2\frontend\src\app\`

## Special Directories

**backend/migrations/:**
- Purpose: Database migration files managed by Alembic
- Generated: Yes (via Alembic)
- Committed: Yes

**frontend/.next/:**
- Purpose: Next.js build output
- Generated: Yes (during build)
- Committed: No

**backend/src/mcp_tools/:**
- Purpose: Model Context Protocol tools for AI integration
- Contains: Various tools for task management and chatbot functionality

---

*Structure analysis: 2026-02-04*