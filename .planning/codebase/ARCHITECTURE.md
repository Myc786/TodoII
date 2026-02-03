# Architecture

**Analysis Date:** 2026-02-03

## Pattern Overview

**Overall:** Full-stack web application with microservice-like separation between frontend and backend

**Key Characteristics:**
- Backend: REST API built with FastAPI
- Frontend: Client-side rendered React application with Next.js
- Database: SQLModel (SQLAlchemy + Pydantic) with PostgreSQL/SQLite support
- Authentication: JWT-based with user isolation

## Layers

**Backend API Layer:**
- Purpose: Expose REST endpoints for data operations
- Location: `backend/src/api/`
- Contains: Route definitions, request/response schemas, API logic
- Depends on: Models, Services, Database
- Used by: Frontend via HTTP requests

**Service Layer:**
- Purpose: Business logic and data operations with user isolation
- Location: `backend/src/services/`
- Contains: TaskService, authentication utilities, data processing
- Depends on: Models, Database session
- Used by: API layer

**Data Layer:**
- Purpose: Database models, relationships, and ORM operations
- Location: `backend/src/models/`
- Contains: SQLModel definitions for Task, User, Tag entities
- Depends on: Database connection
- Used by: Service and API layers

**Frontend Components Layer:**
- Purpose: UI rendering and user interaction
- Location: `frontend/src/components/`
- Contains: Task forms, lists, filters, authentication UI
- Depends on: API client, React hooks
- Used by: Pages

**Frontend State Management:**
- Purpose: Application state and data fetching
- Location: `frontend/src/hooks/`, `frontend/src/lib/`
- Contains: Authentication hooks, API client, type definitions
- Depends on: API endpoints
- Used by: Components and pages

## Data Flow

**Task Creation Flow:**

1. User submits form in `TaskForm` component (`frontend/src/components/task/task-form.tsx`)
2. Frontend calls `apiClient.createTask()` in `DashboardPage` (`frontend/src/app/dashboard/page.tsx`)
3. Request hits `/api/tasks/` POST endpoint in `backend/src/api/routes/tasks.py`
4. Endpoint calls `TaskService.create_task()` with user context
5. Service creates task in database with user_id association
6. Response returns to frontend, updates local state

**Authentication Flow:**

1. User logs in via auth pages (`frontend/src/app/login/page.tsx`)
2. Credentials sent to `/api/auth/login` endpoint
3. Backend validates credentials in `backend/src/api/routes/auth.py`
4. JWT token generated and returned
5. Frontend stores token and redirects to dashboard

**State Management:**
- Frontend: React useState and custom hooks manage local state
- Backend: SQLModel ORM manages database state with session-based transactions
- User isolation: All queries include user_id filters for security

## Key Abstractions

**Task Model:**
- Purpose: Represents a todo item with user ownership
- Examples: `backend/src/models/task.py`
- Pattern: SQLModel with UUID primary keys, optimistic locking via version field

**TaskService:**
- Purpose: Encapsulates business logic for task operations
- Examples: `backend/src/services/task_service.py`
- Pattern: Static methods with user_id validation for isolation

**API Router:**
- Purpose: Organizes endpoints by domain
- Examples: `backend/src/api/routes/`
- Pattern: FastAPI routers with dependency injection

**Frontend API Client:**
- Purpose: Abstracts HTTP requests to backend
- Examples: `frontend/src/lib/api.ts`
- Pattern: Wrapper around fetch with error handling and authentication headers

## Entry Points

**Backend API:**
- Location: `backend/src/main.py`
- Triggers: HTTP requests to various endpoints
- Responsibilities: Initialize FastAPI app, configure middleware, include routes

**Frontend Dashboard:**
- Location: `frontend/src/app/dashboard/page.tsx`
- Triggers: User authentication and navigation
- Responsibilities: Load tasks and tags, handle CRUD operations, manage UI state

**Frontend Layout:**
- Location: `frontend/src/app/layout.tsx`
- Triggers: Initial page load
- Responsibilities: Wrap app with auth and theme providers, initialize context

## Error Handling

**Strategy:** Centralized error handling with HTTP status codes and meaningful messages

**Patterns:**
- Backend: HTTPException with appropriate status codes (400, 401, 404, 409)
- Frontend: Try/catch blocks with user-friendly feedback messages
- Validation: Pydantic models for request/response validation

## Cross-Cutting Concerns

**Logging:** Python logging module with custom configuration in `backend/src/core/logging_config.py`
**Validation:** Pydantic models for request/response validation and SQLModel for database validation
**Authentication:** JWT tokens with middleware in FastAPI and session management in React

---

*Architecture analysis: 2026-02-03*