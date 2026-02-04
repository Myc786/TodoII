# Architecture

**Analysis Date:** 2026-02-04

## Pattern Overview

**Overall:** Full-stack web application with microservice-like architecture

**Key Characteristics:**
- Backend: FastAPI REST API with SQLModel/SQLAlchemy ORM
- Frontend: Next.js 14 with React Server Components
- Database: PostgreSQL with support for other databases via SQLModel
- User isolation: Each user's data is isolated via user_id foreign keys
- Feature-rich: Includes tasks, tags, reminders, recurrence, search, filtering

## Layers

**Frontend (Next.js):**
- Purpose: User interface and client-side logic
- Location: `D:\part2\frontend\`
- Contains: Pages, components, hooks, API calls, styling
- Depends on: Backend API endpoints
- Used by: End users via browser

**Backend API (FastAPI):**
- Purpose: Business logic, data validation, authentication
- Location: `D:\part2\backend\src\api\`
- Contains: Route definitions, request/response schemas
- Depends on: Services, Models, Database
- Used by: Frontend and external clients

**Services Layer:**
- Purpose: Business logic implementation
- Location: `D:\part2\backend\src\services\`
- Contains: Service classes implementing CRUD operations
- Depends on: Models, Database sessions
- Used by: API routes

**Models Layer:**
- Purpose: Data structures and relationships
- Location: `D:\part2\backend\src\models\`
- Contains: SQLModel definitions, enums, schemas
- Depends on: Database (SQLModel/SQLAlchemy)
- Used by: Services, API routes

**Database Layer:**
- Purpose: Data persistence and retrieval
- Location: `D:\part2\backend\src\database\`
- Contains: Database connection, session management
- Depends on: PostgreSQL driver
- Used by: Models, Services

## Data Flow

**Task Creation:**

1. Frontend sends POST request to `/api/tasks/` with task data
2. FastAPI validates request against TaskCreate schema
3. Authentication middleware verifies user JWT token
4. TaskService.create_task() creates task in database with user_id
5. Response returns created TaskRead object to frontend

**Task Retrieval:**

1. Frontend sends GET request to `/api/tasks/`
2. Authentication middleware verifies user
3. TaskService.get_tasks_by_user_id() retrieves user's tasks
4. Database query filters by user_id
5. Response returns list of user's tasks

**State Management:**
- Frontend: React state and Next.js server components
- Backend: Database transactions and session management
- Authentication: JWT tokens stored in cookies/local storage

## Key Abstractions

**Task Model:**
- Purpose: Represents a todo item with rich features
- Examples: `D:\part2\backend\src\models\task.py`
- Pattern: SQLModel with relationships to User, Tags, Reminders

**TaskService:**
- Purpose: Encapsulates business logic for task operations
- Examples: `D:\part2\backend\src\services\task_service.py`
- Pattern: Static methods for CRUD operations with user isolation

**API Routes:**
- Purpose: Expose endpoints with authentication and validation
- Examples: `D:\part2\backend\src\api\routes\tasks.py`
- Pattern: FastAPI routers with dependency injection

## Entry Points

**Backend API:**
- Location: `D:\part2\backend\src\main.py`
- Triggers: HTTP requests to server
- Responsibilities: Initialize FastAPI app, configure middleware, register routes

**Frontend App:**
- Location: `D:\part2\frontend\src\app\layout.tsx`
- Triggers: Browser navigation
- Responsibilities: Set up auth wrapper, theme provider, global providers

## Error Handling

**Strategy:** Comprehensive exception handling with HTTP status codes

**Patterns:**
- FastAPI HTTPExceptions for validation and business logic errors
- Custom error responses with meaningful messages
- Database transaction rollback on failures

## Cross-Cutting Concerns

**Logging:** Python logging module with custom configuration in `D:\part2\backend\src\core\logging_config.py`
**Validation:** Pydantic models for request/response validation
**Authentication:** JWT-based authentication with middleware in `D:\part2\backend\src\api\deps.py`

---

*Architecture analysis: 2026-02-04*