# Tasks: Backend & Database Foundation

**Feature**: Backend & Database Foundation
**Branch**: 001-backend-database-foundation
**Input**: Implementation plan from `/specs/001-backend-database-foundation/plan.md`
**Dependencies**: None

## Phase 1: Setup

### Goal
Initialize project structure and install required dependencies.

### Tasks
- [x] T001 Create backend directory structure per implementation plan
- [x] T002 [P] Create backend/src directory with subdirectories (models, api, database, core)
- [x] T003 [P] Create backend/tests directory with subdirectories (unit, integration, contract)
- [x] T004 [P] Create requirements.txt with FastAPI, SQLModel, psycopg2-binary, python-jose[cryptography], uvicorn
- [x] T005 Create pyproject.toml for project configuration
- [x] T006 Create backend/.env file with template for DATABASE_URL and BETTER_AUTH_SECRET
- [x] T007 Create backend/src/__init__.py files in all subdirectories

## Phase 2: Foundational Components

### Goal
Set up foundational components that all user stories depend on.

### Tasks
- [x] T008 [P] Create database configuration in backend/src/core/config.py
- [x] T009 [P] Create database session management in backend/src/database/session.py
- [x] T010 [P] Create security utilities for JWT handling in backend/src/core/security.py
- [x] T011 Create base model in backend/src/models/__init__.py
- [x] T012 Create database dependency in backend/src/api/deps.py
- [x] T013 Create main FastAPI app in backend/src/main.py
- [x] T014 Create API router initialization in backend/src/api/__init__.py

## Phase 3: User Story 1 - Database Connectivity and Schema (Priority: P1)

### Goal
Establish database connectivity to Neon PostgreSQL and create User and Task models with proper schema.

### Independent Test
Can be fully tested by establishing a connection to the database and performing basic CRUD operations on User and Task records, delivering reliable data persistence capability.

### Tasks
- [x] T015 [P] [US1] Create User model in backend/src/models/user.py with id, email, name, timestamps
- [x] T016 [P] [US1] Create Task model in backend/src/models/task.py with all required attributes including version for optimistic locking
- [x] T017 [US1] Configure database connection using DATABASE_URL from environment
- [x] T018 [US1] Create database tables using SQLModel's create_all method
- [x] T019 [US1] Add proper indexes to Task model (user_id, created_at)
- [x] T020 [US1] Implement proper relationships between User and Task models
- [x] T021 [US1] Add validation constraints to models (email format, name length, title length)
- [x] T022 [US1] Test database connectivity with sample data insertion

## Phase 4: User Story 2 - Task CRUD Operations (Priority: P1)

### Goal
Implement basic CRUD (Create, Read, Update, Delete) operations on tasks through API endpoints.

### Independent Test
Can be fully tested by making HTTP requests to each CRUD endpoint and verifying that the appropriate database operations are performed, delivering complete task management capability.

### Tasks
- [x] T023 [P] [US2] Create Task service in backend/src/services/task_service.py with CRUD operations
- [x] T024 [P] [US2] Create Task schema models in backend/src/models/task_schemas.py for request/response validation
- [x] T025 [US2] Implement GET /api/tasks endpoint to list user's tasks
- [x] T026 [US2] Implement POST /api/tasks endpoint to create new tasks
- [x] T027 [US2] Implement GET /api/tasks/{task_id} endpoint to get specific task
- [x] T028 [US2] Implement PUT /api/tasks/{task_id} endpoint to update tasks
- [x] T029 [US2] Implement DELETE /api/tasks/{task_id} endpoint to delete tasks
- [x] T030 [US2] Add authentication dependency to all task endpoints
- [x] T031 [US2] Implement user isolation - ensure users only see their own tasks
- [x] T032 [US2] Test all CRUD endpoints with authenticated requests

## Phase 5: User Story 3 - Task Toggle Complete (Priority: P1)

### Goal
Implement endpoint to toggle the completion status of tasks.

### Independent Test
Can be fully tested by making HTTP requests to toggle task completion status and verifying the database record is updated, delivering the ability to track task completion.

### Tasks
- [x] T033 [P] [US3] Add toggle completion method to Task service in backend/src/services/task_service.py
- [x] T034 [US3] Implement PATCH /api/tasks/{task_id}/toggle endpoint
- [x] T035 [US3] Ensure toggle endpoint respects user isolation
- [x] T036 [US3] Test toggle endpoint with authenticated requests
- [x] T037 [US3] Verify task completion status flips correctly

## Phase 6: User Story 4 - Input Validation (Priority: P2)

### Goal
Implement proper input validation for task creation and updates according to specified constraints.

### Independent Test
Can be fully tested by sending requests with various invalid inputs and verifying appropriate error responses are returned, delivering robust input validation.

### Tasks
- [x] T038 [P] [US4] Add Pydantic validation to Task schema models for title length (1-200 chars)
- [x] T039 [US4] Add validation for required fields in Task schema models
- [x] T040 [US4] Add custom validation for email format in User model
- [x] T041 [US4] Test validation with invalid inputs (empty title, too long title)
- [x] T042 [US4] Verify appropriate 400 responses for validation errors

## Phase 7: User Story 5 - Error Handling (Priority: P2)

### Goal
Implement proper error responses for common error conditions such as resource not found and bad requests.

### Independent Test
Can be fully tested by triggering various error conditions and verifying appropriate HTTP status codes and error messages are returned, delivering reliable error reporting.

### Tasks
- [x] T043 [P] [US5] Create custom exception handlers for 404 (Not Found) errors
- [x] T044 [US5] Create custom exception handlers for 400 (Bad Request) errors
- [x] T045 [US5] Implement proper 404 responses when task doesn't exist
- [x] T046 [US5] Implement proper 400 responses for validation errors
- [x] T047 [US5] Add 409 Conflict response for optimistic locking failures
- [x] T048 [US5] Test error conditions to verify correct status codes
- [x] T049 [US5] Ensure error messages are user-friendly and informative

## Phase 8: Optimistic Locking Implementation

### Goal
Implement optimistic locking with version numbers to handle concurrent task modifications.

### Tasks
- [x] T050 [P] [US5] Update Task service to implement optimistic locking with version checks
- [x] T051 [US5] Modify UPDATE endpoint to check version before updating
- [x] T052 [US5] Modify toggle endpoint to check version before updating completion status
- [x] T053 [US5] Test concurrent modification scenarios to verify locking works
- [x] T054 [US5] Ensure 409 Conflict responses when version mismatch occurs

## Phase 9: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with documentation, testing, and quality assurance.

### Tasks
- [x] T055 Create API documentation with Swagger/OpenAPI
- [x] T056 Add comprehensive logging to API endpoints
- [x] T057 Implement proper configuration for different environments (dev, prod)
- [x] T058 Add unit tests for all service layer functions
- [x] T059 Add integration tests for all API endpoints
- [x] T060 Perform end-to-end testing of all user stories
- [x] T061 Update README with setup and usage instructions
- [x] T062 Optimize database queries with proper indexing
- [x] T063 Perform security review of JWT implementation
- [x] T064 Run code quality checks and fix any issues

## Dependencies

### User Story Order
1. User Story 1 (Database Connectivity) - Foundation for all other stories
2. User Story 2 (CRUD Operations) - Depends on User Story 1
3. User Story 3 (Toggle Complete) - Depends on User Story 2
4. User Story 4 (Input Validation) - Can run in parallel with other stories
5. User Story 5 (Error Handling) - Can run in parallel with other stories
6. Optimistic Locking - Depends on User Story 2 and 3

### Parallel Execution Examples

**User Story 2 (CRUD Operations)**:
- T023-T024 (Service and schemas) can run in parallel with T025-T029 (Endpoints)
- T030-T032 (Authentication and testing) can run after endpoints are implemented

**User Story 4 & 5 (Validation & Error Handling)**:
- These can be implemented in parallel with other user stories, adding validation and error handling to existing endpoints

## Implementation Strategy

### MVP First Approach
1. Complete Phase 1-3 (Setup + Database connectivity) - Minimum viable foundation
2. Implement basic CRUD operations from Phase 4 (T023-T027) - Core functionality
3. Add authentication to endpoints (T030) - Secure the API
4. Test the basic functionality - Verify MVP works

### Incremental Delivery
- After MVP: Add remaining CRUD operations (DELETE, UPDATE)
- Add toggle functionality (Phase 5)
- Add validation and error handling (Phases 6-7)
- Complete with optimistic locking and polish (Phases 8-9)