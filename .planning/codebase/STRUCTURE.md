# Codebase Structure

**Analysis Date:** 2026-02-03

## Directory Layout

```
part2/
├── backend/              # Backend API server
│   ├── src/
│   │   ├── api/          # API routes and controllers
│   │   │   └── routes/   # Individual route modules
│   │   ├── core/         # Core configurations and utilities
│   │   ├── database/     # Database connections and session management
│   │   ├── models/       # Data models and schemas
│   │   ├── services/     # Business logic services
│   │   └── mcp_tools/    # Model Context Protocol tools
│   ├── migrations/       # Database migration files
│   ├── tests/            # Test files
│   ├── requirements.txt  # Python dependencies
│   └── main.py           # Application entry point
├── frontend/             # Frontend React/Next.js application
│   ├── src/
│   │   ├── app/          # Next.js app directory structure
│   │   │   ├── dashboard/ # Dashboard page
│   │   │   ├── login/    # Authentication pages
│   │   │   └── ...       # Other pages
│   │   ├── components/   # Reusable UI components
│   │   ├── contexts/     # React context providers
│   │   ├── hooks/        # Custom React hooks
│   │   ├── lib/          # Utilities and API clients
│   │   └── styles/       # Global styles
│   ├── package.json      # Node.js dependencies
│   └── tsconfig.json     # TypeScript configuration
├── .planning/            # Planning and analysis documents
│   └── codebase/         # Codebase analysis files
├── specs/                # Feature specifications
└── history/              # Prompt history records and ADRs
```

## Directory Purposes

**backend/:**
- Purpose: Server-side application code
- Contains: FastAPI application, models, services, API routes
- Key files: `main.py`, `requirements.txt`, `src/api/routes/`

**frontend/:**
- Purpose: Client-side application code
- Contains: Next.js pages, React components, hooks, utilities
- Key files: `package.json`, `src/app/layout.tsx`, `src/components/`

**backend/src/api/:**
- Purpose: API route definitions and controller logic
- Contains: Route modules for different domains (tasks, auth, chat)
- Key files: `routes/__init__.py`, `deps.py`

**backend/src/models/:**
- Purpose: Data models and schemas
- Contains: SQLModel definitions for database tables
- Key files: `task.py`, `user.py`, `tag.py`, `task_tag.py`

**backend/src/services/:**
- Purpose: Business logic and data processing
- Contains: Service classes with user-isolated operations
- Key files: `task_service.py`

**frontend/src/components/:**
- Purpose: Reusable UI components
- Contains: Task components, auth components, UI primitives
- Key files: `task/task-list.tsx`, `task/task-form.tsx`, `auth/provider.tsx`

**frontend/src/lib/:**
- Purpose: Utilities and API clients
- Contains: API client, type definitions, helper functions
- Key files: `api.ts`, `types.ts`

## Key File Locations

**Entry Points:**
- `backend/src/main.py`: Backend application startup
- `frontend/src/app/layout.tsx`: Frontend application wrapper
- `frontend/src/app/dashboard/page.tsx`: Main dashboard page

**Configuration:**
- `backend/src/core/config.py`: Backend settings and database configuration
- `frontend/tsconfig.json`: Frontend TypeScript configuration
- `frontend/package.json`: Frontend dependencies

**Core Logic:**
- `backend/src/services/task_service.py`: Task business logic
- `backend/src/api/routes/tasks.py`: Task API endpoints
- `frontend/src/lib/api.ts`: Frontend API client

**Testing:**
- `backend/tests/`: Backend test files
- `frontend/src/__tests__/`: Frontend test files

## Naming Conventions

**Files:**
- Backend: snake_case for Python files (e.g., `task_service.py`, `main.py`)
- Frontend: kebab-case for component files (e.g., `task-list.tsx`, `task-form.tsx`)

**Functions:**
- Backend: snake_case (e.g., `get_tasks_by_user_id`)
- Frontend: camelCase (e.g., `handleTaskCreated`, `loadTasksAndTags`)

**Variables:**
- Backend: snake_case (e.g., `user_id`, `task_create`)
- Frontend: camelCase (e.g., `tasks`, `activeFilter`)

**Types:**
- Backend: PascalCase for classes (e.g., `TaskService`, `TaskCreate`)
- Frontend: PascalCase for types and interfaces (e.g., `Task`, `Tag`)

## Where to Add New Code

**New Feature:**
- Primary code: `backend/src/services/` for backend logic, `frontend/src/components/` for UI
- Tests: `backend/tests/` and `frontend/src/__tests__/`

**New API Endpoint:**
- Backend: Add to appropriate route file in `backend/src/api/routes/`
- Frontend: Add method to API client in `frontend/src/lib/api.ts`

**New Component/Module:**
- Implementation: `frontend/src/components/` for frontend, `backend/src/services/` for backend
- Pages: `frontend/src/app/` for new Next.js pages

**Utilities:**
- Shared helpers: `frontend/src/lib/` for frontend, `backend/src/core/` for backend

## Special Directories

**backend/migrations/:**
- Purpose: Database migration files managed by Alembic
- Generated: Yes, by Alembic commands
- Committed: Yes

**frontend/.next/:**
- Purpose: Next.js build output directory
- Generated: Yes, by Next.js build process
- Committed: No (in .gitignore)

**backend/src/__pycache__/:**
- Purpose: Python bytecode cache
- Generated: Yes, by Python interpreter
- Committed: No (in .gitignore)

**.planning/:**
- Purpose: Project planning and analysis documents
- Generated: By Claude Code planning tools
- Committed: Yes

---

*Structure analysis: 2026-02-03*