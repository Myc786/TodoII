# Coding Conventions

**Analysis Date:** 2026-02-04

## Python Backend Conventions

**Naming:**
- Files: snake_case (e.g., `task_service.py`, `task_schemas.py`)
- Functions: snake_case (e.g., `get_task_by_id`, `create_task`)
- Classes: PascalCase (e.g., `TaskService`, `TaskCreate`)
- Variables: snake_case (e.g., `user_id`, `task_data`)
- Constants: UPPER_SNAKE_CASE (e.g., `API_BASE_URL`)

**Code Style:**
- Formatting: Black formatter with 88 character line length (from pyproject.toml)
- Linting: Flake8 and mypy (from pyproject.toml)
- Type hints: Required for all public functions/methods
- Line length: 88 characters maximum

**Function Design:**
- Functions follow docstring convention with Args/Returns sections
- Error handling primarily through HTTPExceptions in API layer
- Business logic separated in service classes
- Database operations wrapped in services with session management

**Import Organization:**
- Standard library imports first
- Third-party imports second
- Local imports last
- Each group separated by blank lines

**Error Handling:**
- HTTP endpoints raise HTTPException for API errors
- Business logic raises ValueError for validation issues
- Database operations return None/False for not found scenarios
- Proper status codes: 400 for bad requests, 401 for unauthorized, 404 for not found, 409 for conflicts

**Class Design:**
- Service classes use static methods for business logic
- Model classes use SQLModel with Pydantic-style validation
- API routes organized in router modules

## TypeScript Frontend Conventions

**Naming:**
- Files: PascalCase for components (e.g., `TaskCard.tsx`), camelCase for utilities (e.g., `api.ts`)
- Components: PascalCase (e.g., `TaskCard`, `TaskForm`)
- Functions: camelCase (e.g., `getAuthHeaders`, `handleReminderSet`)
- Variables: camelCase (e.g., `taskData`, `onToggle`)
- Types: PascalCase (e.g., `Task`, `TaskCardProps`)

**Code Style:**
- Formatting: Standard Next.js/TypeScript formatting
- Type safety: Strict TypeScript with explicit interfaces
- Hooks: Follow React hooks conventions (useState, useEffect, etc.)
- Component structure: Props interface, component function, JSX return

**Component Design:**
- Functional components with TypeScript interfaces for props
- Client components marked with `'use client'` directive
- Composition over inheritance for UI building
- Utility functions in separate modules (`lib/utils.ts`, `lib/task-helpers.ts`)

**Import Organization:**
- External libraries first (react, lucide-react, etc.)
- UI components with path aliases (`@/components/ui/*`)
- Internal modules with path aliases (`@/lib/*`, `@/components/*`)
- Relative imports for closely related files

**Error Handling:**
- Try/catch blocks in async functions
- Error responses with success/error properties
- Network error handling with specific messaging
- Console.error for debugging purposes

## Cross-Cutting Conventions

**Security:**
- Authorization headers for API requests
- JWT tokens for authentication
- Input validation at API boundaries
- Password hashing with bcrypt

**API Communication:**
- RESTful endpoints following standard conventions
- Consistent response formats
- Proper HTTP status codes
- Versioning through API paths

**Documentation:**
- Comprehensive docstrings in Python functions
- JSDoc-style comments in TypeScript
- Type definitions for all API payloads
- Inline comments for complex logic

---

*Convention analysis: 2026-02-04*