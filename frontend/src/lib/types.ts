// Task Interface - Based on the backend Task model from @specs/database/schema.md
export interface Task {
  id: string; // UUID identifier
  title: string; // Required, 1-200 characters
  description?: string; // Optional
  completed: boolean; // Default: false
  user_id: string; // Foreign key to User
  version: number; // For optimistic locking, default: 1
  created_at: string; // ISO date string
  updated_at: string; // ISO date string
}

// User Session Interface - Represents the authenticated user state
export interface UserSession {
  id: string; // User identifier
  email: string; // User's email address
  name: string; // User's display name
  isAuthenticated: boolean; // Whether user is logged in
  token?: string; // JWT token for API authentication
}

// API Response Types - Standardized response types for API communication
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  success: boolean;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    pageSize: number;
    totalCount: number;
    totalPages: number;
  };
}

// API Request Types - Standardized request types for API communication
export interface CreateTaskRequest {
  title: string;
  description?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  version: number; // Required for optimistic locking
}

export interface ToggleTaskRequest {
  version: number; // Required for optimistic locking
}

// Component Props Types - Types for reusable UI components
export interface TaskCardProps {
  task: Task;
  onToggle: (taskId: string, version: number) => void;
  onUpdate: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
}

export interface TaskFormProps {
  onSubmit: (taskData: CreateTaskRequest) => void;
  onCancel?: () => void;
  initialValues?: Partial<CreateTaskRequest>;
}

export interface TaskListProps {
  tasks: Task[];
  loading?: boolean;
  onToggle: (taskId: string, version: number) => void;
  onUpdate: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
  emptyMessage?: string;
}