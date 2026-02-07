# Research: Todo App Feature Expansion

## Overview
Research conducted to understand the current state of the todo application and plan the implementation of intermediate and advanced features.

## Current State Analysis

### Technology Stack
- **Backend**: Python 3.12, FastAPI, SQLModel, PostgreSQL (Neon), SQLAlchemy
- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS
- **Authentication**: Better Auth with JWT tokens
- **Database**: Neon PostgreSQL with SQLModel ORM

### Existing Features Implemented
- Basic CRUD operations for tasks
- User authentication and authorization
- Task completion toggling with optimistic locking
- Priority levels (high, medium, low)
- Tagging system with many-to-many relationships
- Due date functionality
- Recurrence pattern support (structure in place)
- Frontend components for all advanced features

### Data Models Identified
#### Task Model
- `id`: UUID (primary key)
- `title`: String (1-200 chars, required)
- `description`: Optional string
- `completed`: Boolean (default: false)
- `user_id`: UUID (foreign key to user)
- `version`: Integer (for optimistic locking, default: 1)
- `created_at`: DateTime (with index)
- `updated_at`: DateTime
- `priority`: Optional string (enum: high, medium, low, default: medium)
- `due_date`: Optional DateTime
- `recurrence_pattern`: Optional string (JSON for recurrence rules)
- `original_task_id`: Optional UUID (for recurring tasks)

#### Tag Model
- `id`: UUID (primary key)
- `name`: String (1-50 chars, required)
- `color`: Optional string (hex color code)
- `user_id`: UUID (foreign key to user)
- `created_at`: DateTime (with index)

#### TaskTag Association Model
- `task_id`: UUID (foreign key to task, primary key)
- `tag_id`: UUID (foreign key to tag, primary key)

### API Endpoints Available
- GET `/api/tasks/` - Get all user tasks with pagination
- POST `/api/tasks/` - Create new task
- GET `/api/tasks/{task_id}` - Get specific task
- PUT `/api/tasks/{task_id}` - Update task
- DELETE `/api/tasks/{task_id}` - Delete task
- PATCH `/api/tasks/{task_id}/toggle` - Toggle completion status

### Frontend Components Available
- TaskCard: Displays individual tasks with priority badges, tags, due dates
- TaskForm: Form for creating/updating tasks with priority selector and tag input
- TaskList: List component for displaying multiple tasks
- PrioritySelector: Dropdown for selecting priority levels
- TagInput: Component for selecting and creating tags
- TagManager: Component for managing tags
- TaskFilters: Basic filtering by completion status

## Key Decisions Made

### 1. Priority Implementation
**Decision**: Use string enum for priority levels (high, medium, low)
**Rationale**: Simple to implement and understand, maps directly to UI requirements
**Alternatives considered**:
- Integer values (1, 2, 3) - rejected as less readable
- Separate Priority entity - rejected as overly complex for this use case

### 2. Tag Implementation
**Decision**: Many-to-many relationship between Task and Tag with TaskTag association table
**Rationale**: Flexible, allows multiple tags per task and multiple tasks per tag
**Alternatives considered**:
- JSON field in Task - rejected as it makes querying difficult
- Array field in Task - rejected as it violates normalization principles

### 3. Due Date Implementation
**Decision**: DateTime field in Task model with timezone-aware handling
**Rationale**: Standard approach that fits the requirement
**Alternatives considered**:
- Separate Reminder entity - too complex for basic due date functionality

### 4. Recurrence Implementation
**Decision**: JSON field for recurrence pattern with template-based approach
**Rationale**: Flexible enough to handle various recurrence patterns
**Implementation approach**: Store pattern as JSON, generate new tasks based on template when completed

### 5. Search and Filter Implementation
**Decision**: Backend API endpoints with query parameters for filtering and search
**Rationale**: Maintains separation of concerns, reduces frontend complexity
**Implementation approach**: Extend existing API with additional query parameters

## Implementation Gaps Identified

### Missing Features
1. **Search functionality**: Need to implement keyword search across task titles and descriptions
2. **Advanced filtering**: Need to implement filters for priority, tags, and dates
3. **Sorting functionality**: Need to implement sorting by due date, priority, and alphabetical
4. **Recurrence engine**: Need to implement the logic for generating recurring tasks
5. **Reminder system**: Need to implement notification system for due date reminders

### API Extensions Needed
1. Add search endpoint: `GET /api/tasks/search?q={keyword}`
2. Add advanced filters to existing endpoints: `GET /api/tasks/?priority=high&tag_id=uuid&due_after=date`
3. Add sorting parameters: `GET /api/tasks/?sort_by=priority&order=desc`
4. Add recurrence processing endpoints
5. Add reminder management endpoints

### Frontend Enhancements Needed
1. Advanced filter UI components
2. Search input component
3. Sorting controls
4. Recurrence pattern selection UI
5. Reminder settings UI

## Architecture Considerations

### Scalability
- Use indexes on frequently queried fields (user_id, created_at, priority)
- Implement pagination for large task lists
- Consider caching for frequently accessed data

### Security
- All endpoints properly validate user ownership
- JWT tokens properly validated
- Input validation on all fields

### Performance
- Optimize database queries with proper indexing
- Implement efficient search algorithms
- Use database-level filtering rather than in-memory filtering

## Conclusion
The foundation for intermediate and advanced features is largely in place. The main gaps are in the implementation of search, filtering, sorting, recurrence engine, and reminder system. The data models and basic CRUD operations are already implemented, which significantly reduces the implementation effort.