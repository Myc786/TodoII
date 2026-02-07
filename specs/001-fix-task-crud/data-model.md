# Data Model: Fix Task CRUD Operations

**Feature**: 001-fix-task-crud
**Date**: 2026-02-07
**Status**: No Changes Required

## Overview

This is a bug fix feature. **No data model changes are required.**

The existing Task entity and schema are correctly defined and functioning.

## Existing Task Entity

**Location**: `backend/src/models/task.py` (lines 41-87)

### Fields

| Field | Type | Required | Default | Notes |
|-------|------|----------|---------|-------|
| `id` | UUID | Auto | Generated | Primary key |
| `title` | String(200) | Yes | - | 1-200 characters |
| `description` | String | No | null | Optional details |
| `completed` | Boolean | No | false | Completion status |
| `user_id` | UUID FK | Yes | - | Owner reference |
| `version` | Integer | No | 1 | Optimistic locking |
| `created_at` | DateTime | No | Now | Auto-set |
| `updated_at` | DateTime | No | Now | Auto-updated |
| `priority` | String | No | "medium" | high/medium/low |
| `due_date` | DateTime | No | null | Optional deadline |
| `recurrence_pattern` | String | No | null | JSON recurrence |

### Relationships

- `user`: Many-to-One with User
- `reminders`: One-to-Many with Reminder
- `tags`: Many-to-Many with Tag via TaskTag

## Schema Validation

### TaskUpdate (for PUT operations)

**Location**: `backend/src/models/task_schemas.py` (lines 41-50)

```python
class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None
    recurrence_pattern: Optional[str] = None
    tag_ids: Optional[List[str]] = None
    version: Optional[int] = None  # Optimistic locking
```

### TaskToggle (for PATCH toggle operations)

**Location**: `backend/src/models/task_schemas.py` (lines 53-55)

```python
class TaskToggle(SQLModel):
    version: int  # Required for optimistic locking
```

## Frontend Types

**Location**: `frontend/src/lib/types.ts`

### UpdateTaskRequest (lines 93-102)

```typescript
export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: string;
  due_date?: string;
  recurrence_pattern?: string;
  tag_ids?: string[];
  version: number;  // Required
}
```

### ToggleTaskRequest (lines 115-117)

```typescript
export interface ToggleTaskRequest {
  version: number;  // Required
}
```

## Conclusion

All data models and schemas are correctly implemented. The bug is in the frontend component logic, not the data layer.
