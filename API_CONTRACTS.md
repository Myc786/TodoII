# API Contracts: Vercel-HF Integration

## Overview
This document defines the API contracts between the Vercel-hosted frontend and Hugging Face Spaces backend for the Todo application.

## Authentication API

### POST /api/auth/login
Authenticate user and retrieve JWT token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "user_password"
}
```

**Response (200 OK):**
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "uuid_string",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**Error Responses:**
- 400: Bad Request - Missing email or password
- 401: Unauthorized - Invalid credentials
- 422: Validation Error - Invalid input format

### POST /api/auth/register
Register a new user account

**Request:**
```json
{
  "email": "user@example.com",
  "name": "Full Name",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "id": "uuid_string",
  "email": "user@example.com",
  "name": "Full Name",
  "created_at": "2023-01-01T00:00:00Z"
}
```

**Error Responses:**
- 400: Bad Request - Invalid input
- 409: Conflict - User already exists
- 422: Validation Error - Validation failed

### GET /api/auth/me
Get current authenticated user profile

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "id": "uuid_string",
  "email": "user@example.com",
  "name": "User Name",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Error Responses:**
- 401: Unauthorized - Invalid or expired token

## Task API

### GET /api/tasks
Retrieve list of tasks for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Query Parameters:**
- `limit` (optional, default: 50): Maximum number of tasks to return
- `offset` (optional, default: 0): Number of tasks to skip
- `completed` (optional): Filter by completion status (true/false)
- `sort_by` (optional): Field to sort by ('created_at', 'updated_at', 'title')
- `order` (optional, default: 'desc'): Sort order ('asc', 'desc')

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": "uuid_string",
      "title": "Task Title",
      "description": "Task description",
      "completed": false,
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z",
      "version": 1,
      "priority": "medium",
      "due_date": "2023-01-15T00:00:00Z",
      "tags": [
        {
          "id": "uuid_string",
          "name": "tag_name",
          "color": "#FF5733"
        }
      ]
    }
  ],
  "total": 1,
  "offset": 0,
  "limit": 50
}
```

### POST /api/tasks
Create a new task

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request:**
```json
{
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "priority": "medium",
  "due_date": "2023-01-15T00:00:00Z",
  "tags": ["work", "important"]
}
```

**Response (201 Created):**
```json
{
  "id": "uuid_string",
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z",
  "version": 1,
  "priority": "medium",
  "due_date": "2023-01-15T00:00:00Z",
  "tags": [
    {
      "id": "uuid_string",
      "name": "work",
      "color": "#3498DB"
    }
  ]
}
```

**Error Responses:**
- 400: Bad Request - Invalid input
- 401: Unauthorized - Invalid token
- 422: Validation Error - Validation failed

### PUT /api/tasks/{id}
Update an existing task

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Path Parameters:**
- `id` (required): Task ID

**Request:**
```json
{
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true,
  "priority": "high",
  "due_date": "2023-01-20T00:00:00Z",
  "version": 1
}
```

**Response (200 OK):**
```json
{
  "id": "uuid_string",
  "title": "Updated Task Title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z",
  "version": 2,
  "priority": "high",
  "due_date": "2023-01-20T00:00:00Z",
  "tags": [
    {
      "id": "uuid_string",
      "name": "work",
      "color": "#3498DB"
    }
  ]
}
```

**Error Responses:**
- 400: Bad Request - Invalid input or version mismatch
- 401: Unauthorized - Invalid token
- 404: Not Found - Task doesn't exist
- 409: Conflict - Optimistic lock error (version mismatch)
- 422: Validation Error - Validation failed

### DELETE /api/tasks/{id}
Delete a task

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Path Parameters:**
- `id` (required): Task ID

**Response (204 No Content):**

**Error Responses:**
- 401: Unauthorized - Invalid token
- 404: Not Found - Task doesn't exist
- 422: Validation Error - Validation failed

### PUT /api/tasks/{id}/toggle
Toggle task completion status

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Path Parameters:**
- `id` (required): Task ID

**Request:**
```json
{
  "version": 1
}
```

**Response (200 OK):**
```json
{
  "id": "uuid_string",
  "title": "Task Title",
  "completed": true,
  "updated_at": "2023-01-02T00:00:00Z",
  "version": 2
}
```

**Error Responses:**
- 400: Bad Request - Invalid input or version mismatch
- 401: Unauthorized - Invalid token
- 404: Not Found - Task doesn't exist
- 409: Conflict - Optimistic lock error (version mismatch)

## Tag API

### GET /api/tags
Retrieve list of tags for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
[
  {
    "id": "uuid_string",
    "name": "work",
    "color": "#3498DB",
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

### POST /api/tags
Create a new tag

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request:**
```json
{
  "name": "personal",
  "color": "#E74C3C"
}
```

**Response (201 Created):**
```json
{
  "id": "uuid_string",
  "name": "personal",
  "color": "#E74C3C",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

## Chat API

### POST /api/chat
Process natural language commands

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request:**
```json
{
  "message": "Create a task called 'Buy groceries'"
}
```

**Response (200 OK):**
```json
{
  "message": "I've created the task 'Buy groceries' for you.",
  "success": true,
  "action": "task_created",
  "task_id": "uuid_string"
}
```

## Health Check API

### GET /health
Check the health status of the backend

**Response (200 OK):**
```json
{
  "status": "healthy",
  "environment": "production"
}
```

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Error message explaining what went wrong"
}
```

Or for validation errors:

```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "Field required",
      "type": "missing"
    }
  ]
}
```

## Common Headers

### Authorization Header
All authenticated endpoints require:
```
Authorization: Bearer {jwt_token}
```

### Content-Type Header
For POST/PUT requests:
```
Content-Type: application/json
```

## Rate Limiting
The API implements rate limiting to prevent abuse:
- 100 requests per minute per IP for public endpoints
- 1000 requests per minute per user for authenticated endpoints
- Exceeding limits results in 429 Too Many Requests response

## Versioning
This API follows semantic versioning. Breaking changes will increment the major version number. Backwards-compatible changes increment the minor version. The API currently uses version 1.0.0, indicated by the /api/v1 prefix (which is implicit in the current endpoints).