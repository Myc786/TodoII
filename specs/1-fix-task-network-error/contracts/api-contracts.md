# API Contracts: Task Creation and Authentication

## Task Creation Endpoint
```
POST /api/tasks/
```

### Request
- **Headers**:
  - `Authorization: Bearer {token}` (required)
  - `Content-Type: application/json`
- **Body**:
  ```json
  {
    "title": "string (required, 1-200 chars)",
    "description": "string (optional)",
    "priority": "string (optional, high/medium/low)",
    "due_date": "string (optional, ISO date)",
    "recurrence_pattern": "string (optional, JSON)",
    "tag_ids": "string[] (optional)"
  }
  ```

### Responses
- **200 OK**: Task created successfully
  ```json
  {
    "id": "uuid",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "user_id": "uuid",
    "version": "number",
    "created_at": "iso-date-string",
    "updated_at": "iso-date-string",
    "priority": "string",
    "due_date": "iso-date-string",
    "recurrence_pattern": "string",
    "original_task_id": "uuid",
    "tags": "Tag[]"
  }
  ```
- **400 Bad Request**: Validation error
- **401 Unauthorized**: Invalid or missing authentication token
- **422 Unprocessable Entity**: Malformed request

## Authentication Verification
```
GET /api/auth/me
```

### Request
- **Headers**:
  - `Authorization: Bearer {token}` (required)

### Responses
- **200 OK**: Valid token, returns user info
- **401 Unauthorized**: Invalid token

## Error Response Format
```json
{
  "detail": "error message"
}
```