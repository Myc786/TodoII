# Data Model: Backend & Database Foundation

## User Entity
- **id**: UUID/string (primary key)
- **email**: string (unique, required for authentication)
- **name**: string (user display name, required)
- **created_at**: datetime (timestamp when user was created)
- **updated_at**: datetime (timestamp when user was last updated)

### Relationships
- User has many Tasks (one-to-many)

### Validation Rules
- Email must be a valid email format
- Name must be 1-100 characters
- Email must be unique across all users

## Task Entity
- **id**: UUID/string (primary key)
- **title**: string (required, 1-200 characters)
- **description**: string (optional, no specific length limit)
- **completed**: boolean (default: false)
- **user_id**: UUID/string (foreign key to User)
- **version**: integer (for optimistic locking, default: 1)
- **created_at**: datetime (timestamp when task was created)
- **updated_at**: datetime (timestamp when task was last updated)

### Relationships
- Task belongs to one User (many-to-one)

### Validation Rules
- Title must be 1-200 characters
- Description is optional
- Completed defaults to false
- user_id must reference an existing User
- version must be incremented on each update

### State Transitions
- Task starts with completed=False
- Task can be toggled to completed=True
- Task can be toggled back to completed=False
- Task can be updated (with version increment)
- Task can be deleted (soft delete with deleted_at timestamp)

## Database Schema Considerations
- Use UUIDs for primary keys to avoid predictability
- Add indexes on user_id for efficient querying by user
- Add indexes on created_at for chronological sorting
- Implement soft deletes using deleted_at field if needed for audit trail
- Use optimistic locking via version column to handle concurrent updates