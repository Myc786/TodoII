# Data Model: Frontend UI & API Integration

## Task Interface
Based on the backend Task model from @specs/database/schema.md:

```typescript
interface Task {
  id: string; // UUID identifier
  title: string; // Required, 1-200 characters
  description?: string; // Optional
  completed: boolean; // Default: false
  userId: string; // Foreign key to User
  version: number; // For optimistic locking, default: 1
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}
```

### Validation Rules
- Title must be 1-200 characters
- Description is optional
- Completed defaults to false
- userId must correspond to an existing user
- version must be incremented on each update

### State Transitions
- Task starts with completed=false
- Task can be toggled to completed=true
- Task can be toggled back to completed=false
- Task can be updated (with version increment)
- Task can be deleted (removed from UI)

## User Session Interface
Represents the authenticated user state:

```typescript
interface UserSession {
  id: string; // User identifier
  email: string; // User's email address
  name: string; // User's display name
  isAuthenticated: boolean; // Whether user is logged in
  token?: string; // JWT token for API authentication
}
```

## API Response Types
Standardized response types for API communication:

```typescript
interface ApiResponse<T> {
  data?: T;
  error?: string;
  success: boolean;
}

interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    pageSize: number;
    totalCount: number;
    totalPages: number;
  };
}
```

## API Request Types
Standardized request types for API communication:

```typescript
interface CreateTaskRequest {
  title: string;
  description?: string;
}

interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  version: number; // Required for optimistic locking
}

interface ToggleTaskRequest {
  version: number; // Required for optimistic locking
}
```

## Component Props Types
Types for reusable UI components:

```typescript
interface TaskCardProps {
  task: Task;
  onToggle: (taskId: string, version: number) => void;
  onUpdate: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
}

interface TaskFormProps {
  onSubmit: (taskData: CreateTaskRequest) => void;
  onCancel?: () => void;
  initialValues?: Partial<CreateTaskRequest>;
}

interface TaskListProps {
  tasks: Task[];
  loading?: boolean;
  onToggle: (taskId: string, version: number) => void;
  onUpdate: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
  emptyMessage?: string;
}
```