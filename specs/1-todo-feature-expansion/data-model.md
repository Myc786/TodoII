# Data Model: Todo App Feature Expansion

## Overview
This document describes the data models for the intermediate and advanced features of the todo application. The models extend the existing basic task functionality with priority, tags, due dates, recurrence, and search/filter capabilities.

## Core Entities

### Task Entity
The Task entity represents a single todo item with enhanced capabilities for organization and automation.

```sql
-- Table: task
-- Primary entity for todo items with enhanced features
```

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the task |
| title | VARCHAR(200) | NOT NULL, LENGTH >= 1 | Title of the task (1-200 characters) |
| description | TEXT | NULLABLE | Optional description of the task |
| completed | BOOLEAN | DEFAULT FALSE | Boolean indicating if the task is completed |
| user_id | UUID | FOREIGN KEY(user.id), INDEX | Foreign key linking to the user who owns this task |
| version | INTEGER | DEFAULT 1 | Integer for optimistic locking |
| created_at | TIMESTAMP | INDEX, DEFAULT NOW() | Timestamp when the task was created |
| updated_at | TIMESTAMP | NULLABLE | Timestamp when the task was last updated |
| priority | VARCHAR(10) | DEFAULT 'medium', ENUM('high','medium','low') | Priority level of the task |
| due_date | TIMESTAMP | NULLABLE | Due date for the task |
| recurrence_pattern | TEXT | NULLABLE | JSON defining recurrence rules if task repeats |
| original_task_id | UUID | FOREIGN KEY(task.id) | Links to template for recurring instances |

#### Relationships
- **Many-to-One**: Task belongs to User (via user_id)
- **Many-to-Many**: Task connects to Tags (via TaskTag association)
- **Self-Reference**: Task may reference another Task (via original_task_id for recurring tasks)

#### Validation Rules
- Title: 1-200 characters, required
- Priority: Must be one of 'high', 'medium', 'low'
- Due date: Must be a valid future date if provided
- User isolation: Only accessible by owning user

### Tag Entity
The Tag entity represents a category or label that can be applied to tasks for organization.

```sql
-- Table: tag
-- Entity for task categorization and grouping
```

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY, NOT NULL | Unique identifier for the tag |
| name | VARCHAR(50) | NOT NULL, LENGTH >= 1 | Name of the tag (1-50 characters) |
| color | VARCHAR(7) | NULLABLE | Hex color code for visual representation |
| user_id | UUID | FOREIGN KEY(user.id), INDEX | Foreign key linking to the user who owns this tag |
| created_at | TIMESTAMP | INDEX, DEFAULT NOW() | Timestamp when the tag was created |

#### Relationships
- **Many-to-One**: Tag belongs to User (via user_id)
- **Many-to-Many**: Tag connects to Tasks (via TaskTag association)

#### Validation Rules
- Name: 1-50 characters, required
- Color: Must be valid hex color code (#RRGGBB) if provided
- User isolation: Only accessible by owning user

### TaskTag Association Entity
The TaskTag entity implements the many-to-many relationship between Task and Tag entities.

```sql
-- Table: task_tag
-- Association table for many-to-many relationship between Task and Tag
```

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| task_id | UUID | PRIMARY KEY, FOREIGN KEY(task.id) | Foreign key referencing the task |
| tag_id | UUID | PRIMARY KEY, FOREIGN KEY(tag.id) | Foreign key referencing the tag |

#### Relationships
- **One-to-Many**: TaskTag connects to Task (via task_id)
- **One-to-Many**: TaskTag connects to Tag (via tag_id)

## Enhanced Features Data Structures

### Priority Enumeration
The PriorityLevel enum defines valid values for task priority.

```python
class PriorityLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
```

### Recurrence Pattern Structure
The recurrence_pattern field stores a JSON object defining how a task should repeat.

```json
{
  "type": "daily|weekly|monthly|custom",
  "interval": 1,
  "days_of_week": [0, 1, 2, 3, 4], // For weekly: 0=Sunday, 1=Monday, etc.
  "day_of_month": 15, // For monthly
  "end_date": "2023-12-31", // Optional end condition
  "occurrences": 10 // Optional occurrence limit
}
```

### Search and Filter Parameters
Query parameters for enhanced search and filtering capabilities.

| Parameter | Type | Description |
|-----------|------|-------------|
| q | string | Keyword search term for title/description |
| status | string | Filter by completion status: 'active', 'completed', 'all' |
| priority | string | Filter by priority: 'high', 'medium', 'low' |
| tag_ids | array | Filter by tag IDs |
| due_before | date | Filter tasks due before specified date |
| due_after | date | Filter tasks due after specified date |
| sort_by | string | Sort by: 'due_date', 'priority', 'created_at', 'title' |
| order | string | Sort order: 'asc', 'desc' |

## API Contract Definitions

### Task Creation Request
```json
{
  "title": "string (required, 1-200 chars)",
  "description": "string (optional)",
  "priority": "string (high, medium, low, default: medium)",
  "due_date": "string (ISO 8601 date format, optional)",
  "recurrence_pattern": "string (JSON, optional)",
  "tag_ids": "array of string (UUIDs, optional)"
}
```

### Task Response
```json
{
  "id": "string (UUID)",
  "title": "string",
  "description": "string",
  "completed": "boolean",
  "user_id": "string (UUID)",
  "version": "integer",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601)",
  "priority": "string",
  "due_date": "string (ISO 8601) or null",
  "recurrence_pattern": "string (JSON) or null",
  "original_task_id": "string (UUID) or null",
  "tags": "array of Tag objects"
}
```

### Tag Response
```json
{
  "id": "string (UUID)",
  "name": "string",
  "color": "string (hex) or null",
  "user_id": "string (UUID)",
  "created_at": "string (ISO 8601)"
}
```

## State Transitions

### Task State Transitions
- **Active** → **Completed**: When user marks task as complete
- **Completed** → **Active**: When user unmarks task as complete
- **Created** → **Active**: When new task is created (default state)

### Priority Changes
- Priority can be updated at any time regardless of completion status
- Priority changes do not affect other task states

## Indexes for Performance

### Required Indexes
- `idx_task_user_id`: On `user_id` column for user isolation queries
- `idx_task_created_at`: On `created_at` column for chronological ordering
- `idx_task_priority`: On `priority` column for priority-based filtering
- `idx_task_due_date`: On `due_date` column for due date queries
- `idx_task_completed`: On `completed` column for status filtering

### Composite Indexes
- `idx_task_user_priority`: On `(user_id, priority)` for user + priority queries
- `idx_task_user_status`: On `(user_id, completed)` for user + status queries
- `idx_task_user_due_date`: On `(user_id, due_date)` for user + due date queries

## Migration Strategy

### Backward Compatibility
- All new fields are nullable with sensible defaults
- Existing basic functionality remains unchanged
- No breaking changes to existing API endpoints

### Forward Compatibility
- New API endpoints added alongside existing ones
- Query parameters for new features are optional
- Default behavior preserved for existing clients