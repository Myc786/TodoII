# Frontend API Contracts: Todo Application

## API Client Interface

### Base Configuration
```typescript
const API_CONFIG = {
  BASE_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  HEADERS: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer {token}',
  },
};
```

### Task Endpoints

#### GET /tasks
**Purpose**: Fetch all tasks for the authenticated user
**Method**: GET
**Headers**: Authorization: Bearer {token}
**Query Parameters**:
- skip (optional): number of records to skip for pagination
- limit (optional): max number of records to return
**Response**: `Array<Task>`
**Expected Status Codes**: 200 (success), 401 (unauthorized), 500 (server error)

#### POST /tasks
**Purpose**: Create a new task
**Method**: POST
**Headers**: Authorization: Bearer {token}
**Body**: `{ title: string, description?: string }`
**Response**: `Task`
**Expected Status Codes**: 201 (created), 400 (validation error), 401 (unauthorized), 422 (unprocessable entity)

#### GET /tasks/{task_id}
**Purpose**: Get a specific task
**Method**: GET
**Headers**: Authorization: Bearer {token}
**Response**: `Task`
**Expected Status Codes**: 200 (success), 401 (unauthorized), 404 (not found), 422 (invalid id)

#### PUT /tasks/{task_id}
**Purpose**: Update a specific task
**Method**: PUT
**Headers**: Authorization: Bearer {token}
**Body**: `{ title?: string, description?: string, completed?: boolean, version: number }`
**Response**: `Task`
**Expected Status Codes**: 200 (success), 400 (validation error), 401 (unauthorized), 404 (not found), 409 (conflict - version mismatch), 422 (invalid id)

#### PATCH /tasks/{task_id}/toggle
**Purpose**: Toggle the completion status of a task
**Method**: PATCH
**Headers**: Authorization: Bearer {token}
**Body**: `{ version: number }`
**Response**: `Task`
**Expected Status Codes**: 200 (success), 401 (unauthorized), 404 (not found), 409 (conflict - version mismatch), 422 (invalid id)

#### DELETE /tasks/{task_id}
**Purpose**: Delete a specific task
**Method**: DELETE
**Headers**: Authorization: Bearer {token}
**Expected Status Codes**: 204 (deleted), 401 (unauthorized), 404 (not found), 422 (invalid id)

### Health Check Endpoint

#### GET /health
**Purpose**: Check API health status
**Method**: GET
**Response**: `{ status: string, environment: string }`
**Expected Status Codes**: 200 (success), 500 (server error)

## TypeScript Interfaces

### Task Interface
```typescript
interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  user_id: string;
  version: number;
  created_at: string;
  updated_at: string;
}
```

### API Response Types
```typescript
interface ApiResponse<T> {
  data?: T;
  error?: string;
  success: boolean;
}

interface CreateTaskRequest {
  title: string;
  description?: string;
}

interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  version: number;
}

interface ToggleTaskRequest {
  version: number;
}
```

## Error Handling

### Expected Error Responses
- **400 Bad Request**: `{ detail: string }` - Validation errors
- **401 Unauthorized**: `{ detail: string }` - Missing or invalid JWT token
- **404 Not Found**: `{ detail: string }` - Resource not found
- **409 Conflict**: `{ detail: string }` - Optimistic locking conflict
- **500 Internal Server Error**: `{ detail: string }` - Unexpected server error

## Authentication
All endpoints (except health check) require a valid JWT token in the Authorization header:
```
Authorization: Bearer {jwt_token}
```

The token should be obtained through the authentication system and refreshed as needed.