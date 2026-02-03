# Coding Conventions

**Analysis Date:** 2026-02-03

## Naming Patterns

**Files:**
- Python: snake_case (e.g., `task_service.py`, `task_schemas.py`)
- TypeScript/React: kebab-case or PascalCase (e.g., `task-card.tsx`, `TaskForm.tsx`)

**Functions:**
- Python: snake_case (e.g., `get_tasks_by_user_id`, `create_task`)
- TypeScript: camelCase (e.g., `getAuthHeaders`, `createTask`)

**Variables:**
- Python: snake_case (e.g., `db_task`, `task_data`)
- TypeScript: camelCase (e.g., `taskData`, `apiClient`)

**Types:**
- TypeScript: PascalCase (e.g., `Task`, `ApiResponse`, `CreateTaskRequest`)

## Code Style

**Formatting:**
- Python: Black formatter used (line length 88, Python 3.11 target)
- TypeScript: Standard Next.js/React conventions with Prettier (likely used)

**Linting:**
- Python: MyPy for type checking, flake8 for style checking
- TypeScript: Likely ESLint through Next.js defaults

## Import Organization

**Python:**
- Standard library imports first
- Third-party imports second
- Local application imports last
- Imports grouped with blank lines between groups

**TypeScript:**
- React and React-related imports first
- Third-party libraries next
- Local imports last
- Absolute imports using `@/` alias (e.g., `@/components/ui/button`)

## Error Handling

**Python:**
- Exceptions raised with descriptive messages
- Optimistic locking with version checking
- Validation through Pydantic models
- Database session management with commit/rollback patterns

**TypeScript:**
- Try/catch blocks with error wrapping
- ApiResponse interface for consistent error handling
- HTTP status code checks (401 redirects to login)
- Error message extraction from response bodies

## Logging

**Framework:** Custom logging configuration with Python logging module

**Patterns:**
- Structured logging with levels (INFO, ERROR, DEBUG)
- Context-rich messages with relevant identifiers
- API request/response logging for debugging

## Comments

**When to Comment:**
- Complex business logic explanations
- API endpoint documentation
- Important architectural decisions inline
- TODO/FIXME markers for future work

**JSDoc/TSDoc:**
- Docstrings for Python functions and classes following Google style
- Type annotations used extensively in both Python and TypeScript

## Function Design

**Size:** Functions kept relatively small and focused (single responsibility)
- Python functions typically 10-30 lines
- TypeScript functions typically 10-25 lines

**Parameters:**
- Python: Type hints using Union, Optional, List, Dict
- TypeScript: Strict typing with interfaces and type definitions

**Return Values:**
- Python: Explicit return statements, None for no value
- TypeScript: Consistent return types using ApiResponse pattern

## Module Design

**Exports:**
- Python: Classes and functions exported directly
- TypeScript: Named exports for components/functions, default export for main component

**Barrel Files:**
- Not extensively used in this codebase, but some index.ts files exist

---

*Convention analysis: 2026-02-03*