# Data Model: Todo App Feature Expansion

**Feature**: Todo App Feature Expansion
**Date**: 2026-02-02

## Entity Definitions

### Task (Updated)
**Description**: Represents a single task with enhanced organizational features
- **id**: UUID (Primary Key) - Unique identifier for the task
- **title**: String (1-200 chars) - Title of the task
- **description**: String (Nullable) - Optional description of the task
- **completed**: Boolean - Indicates if the task is completed
- **user_id**: UUID (Foreign Key) - Links to the user who owns this task
- **version**: Integer - For optimistic locking (default: 1)
- **created_at**: DateTime - Timestamp when the task was created
- **updated_at**: DateTime - Timestamp when the task was last updated
- **priority**: String (Enum: 'high', 'medium', 'low') - Task priority level
- **due_date**: DateTime (Nullable) - Date when the task is due
- **recurrence_pattern**: JSON (Nullable) - Defines recurrence rules if task repeats
- **original_task_id**: UUID (Nullable, Foreign Key) - Links to template for recurring instances

**Relationships**:
- One-to-Many: User → Task (via user_id)
- Many-to-Many: Task ↔ Tag (via TaskTag association)

**Validation Rules**:
- Title must be 1-200 characters
- Priority must be one of 'high', 'medium', 'low'
- Due date must be in the future if provided
- Recurrence pattern must follow defined schema if provided

### Tag
**Description**: Represents a category or label that can be applied to tasks
- **id**: UUID (Primary Key) - Unique identifier for the tag
- **name**: String (1-50 chars) - Name of the tag
- **color**: String (Nullable) - Color code for visual representation
- **user_id**: UUID (Foreign Key) - Links to the user who owns this tag
- **created_at**: DateTime - Timestamp when the tag was created

**Relationships**:
- One-to-Many: User → Tag (via user_id)
- Many-to-Many: Tag ↔ Task (via TaskTag association)

**Validation Rules**:
- Name must be 1-50 characters
- Name must be unique per user
- Color must be a valid hex color code if provided

### TaskTag (Association Table)
**Description**: Junction table for the many-to-many relationship between Task and Tag
- **task_id**: UUID (Foreign Key) - References the task
- **tag_id**: UUID (Foreign Key) - References the tag

**Relationships**:
- Many-to-One: TaskTag → Task
- Many-to-One: TaskTag → Tag

**Constraints**:
- Composite primary key: (task_id, tag_id)
- Prevents duplicate associations

### RecurringTaskTemplate
**Description**: Template that defines recurrence rules for recurring tasks
- **id**: UUID (Primary Key) - Unique identifier for the template
- **original_task_data**: JSON - Original task data to use for generating instances
- **recurrence_rule**: JSON - Rule defining how the task should repeat
- **next_occurrence**: DateTime (Nullable) - When the next instance should be created
- **is_active**: Boolean - Whether the recurrence should continue
- **created_at**: DateTime - When the template was created

**Validation Rules**:
- Recurrence rule must follow defined schema
- Next occurrence must be in the future if provided

## State Transitions

### Task States
- **Active**: Task exists but not completed
- **Completed**: Task marked as done
- **Archived**: Task completed and moved to archive (future feature)

**Transitions**:
- Active ↔ Completed (via toggle completion)
- Active → Deleted (via deletion)
- Completed → Deleted (via deletion)

### Recurring Task Lifecycle
- **Template Created**: When a recurring task is first defined
- **Instance Generated**: When a new task instance is created from template
- **Instance Completed**: When an instance is marked complete, triggers next instance generation
- **Template Deactivated**: When recurrence should stop

## Database Schema Changes

### Additions to Existing Tables
```sql
-- Add columns to existing Task table
ALTER TABLE task ADD COLUMN priority VARCHAR(10) DEFAULT 'medium';
ALTER TABLE task ADD COLUMN due_date TIMESTAMP NULL;
ALTER TABLE task ADD COLUMN recurrence_pattern JSON NULL;
ALTER TABLE task ADD COLUMN original_task_id UUID NULL REFERENCES task(id);
```

### New Tables
```sql
-- Create Tag table
CREATE TABLE tag (
    id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) NULL,
    user_id UUID NOT NULL REFERENCES user(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create TaskTag association table
CREATE TABLE task_tag (
    task_id UUID NOT NULL REFERENCES task(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
    PRIMARY KEY (task_id, tag_id)
);

-- Create RecurringTaskTemplate table
CREATE TABLE recurring_task_template (
    id UUID PRIMARY KEY,
    original_task_data JSON NOT NULL,
    recurrence_rule JSON NOT NULL,
    next_occurrence TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Indexes
```sql
-- Existing indexes
CREATE INDEX idx_task_user_id ON task(user_id);
CREATE INDEX idx_task_created_at ON task(created_at);

-- New indexes for performance
CREATE INDEX idx_task_priority ON task(priority);
CREATE INDEX idx_task_due_date ON task(due_date);
CREATE INDEX idx_task_completed ON task(completed);
CREATE INDEX idx_tag_user_id ON tag(user_id);
CREATE INDEX idx_task_tag_task_id ON task_tag(task_id);
CREATE INDEX idx_task_tag_tag_id ON task_tag(tag_id);
```

## API Contract Changes

### Task Model Updates
The Task model will now include:
- `priority` field (string enum)
- `due_date` field (datetime nullable)
- `tags` field (array of tag objects)

### Enhanced Endpoints
- GET /api/tasks?priority=high&tag=work&due_before=2023-12-31 - Filter tasks
- POST /api/tags - Create new tag
- GET /api/tags - List user's tags
- PUT /api/tasks/{id}/tags - Update task tags
- POST /api/tasks/search?q=search_term - Search tasks