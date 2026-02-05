# Data Model Summary: Vercel-HF Integration

## Entities Overview

This integration connects existing frontend and backend systems without introducing new data models. It ensures compatibility between the data schemas used by both systems.

## Task Entity

### Fields
- `id` (UUID): Unique identifier for the task
- `title` (string): Task title (required)
- `description` (string): Task description (optional)
- `completed` (boolean): Completion status
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp
- `version` (int): Optimistic locking version number

### Relationships
- Task belongs to a User (many-to-one)

## User Entity

### Fields
- `id` (UUID): Unique identifier for the user
- `email` (string): User email address (unique, required)
- `name` (string): User name (required)
- `password` (string): Hashed password (required)
- `created_at` (datetime): Account creation timestamp
- `updated_at` (datetime): Last update timestamp

### Relationships
- User has many Tasks (one-to-many)

## Tag Entity

### Fields
- `id` (UUID): Unique identifier for the tag
- `name` (string): Tag name (required, unique per user)
- `color` (string): Display color (optional)
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### Relationships
- Tag belongs to a User (many-to-one)
- Tag has many TaskTag relationships (many-to-many via junction table)

## Reminder Entity

### Fields
- `id` (UUID): Unique identifier for the reminder
- `task_id` (UUID): Reference to associated task
- `scheduled_time` (datetime): When to send reminder
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### Relationships
- Reminder belongs to a Task (many-to-one)

## RecurringTask Entity

### Fields
- `id` (UUID): Unique identifier for recurring task
- `original_task_id` (UUID): Reference to original task
- `pattern` (string): Recurrence pattern
- `interval` (int): Recurrence interval
- `ends_on` (datetime): When recurrence ends
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last update timestamp

### Relationships
- RecurringTask references Original Task (one-to-one)

## API Request/Response Schemas

### Task Creation Request
```
{
  "title": "Task title (required)",
  "description": "Task description (optional)",
  "completed": false,
  "priority": "low|medium|high|urgent",
  "due_date": "ISO 8601 datetime (optional)",
  "tags": ["tag1", "tag2"]
}
```

### Task Response
```
{
  "id": "UUID string",
  "title": "Task title",
  "description": "Task description",
  "completed": false,
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime",
  "version": 1,
  "priority": "low|medium|high|urgent",
  "due_date": "ISO 8601 datetime (or null)",
  "tags": [{"id": "UUID", "name": "tag name", "color": "hex color"}]
}
```

### Authentication Request
```
{
  "email": "user@example.com",
  "password": "user password"
}
```

### Authentication Response
```
{
  "access_token": "JWT token string",
  "token_type": "bearer",
  "user": {
    "id": "UUID string",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

## Validation Rules

### Task Validation
- Title must be 1-255 characters
- Description can be up to 1000 characters
- Priority must be one of: "low", "medium", "high", "urgent"
- Due date must be in the future if provided

### User Validation
- Email must be valid and unique
- Name must be 1-100 characters
- Password must be at least 8 characters
- Email verification required for new accounts

### Tag Validation
- Name must be 1-50 characters
- Color must be valid hex format or null
- Tag names are unique per user

## State Transitions

### Task States
- Pending → Completed (via toggle completion)
- Completed → Pending (via toggle completion)
- Any state → Deleted (via deletion endpoint)

### User Session States
- Anonymous → Authenticated (via login)
- Authenticated → Anonymous (via logout)
- Authenticated → Authenticated (via token refresh)