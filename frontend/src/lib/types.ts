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
  priority?: string; // Priority level (high, medium, low)
  due_date?: string; // Due date string (ISO format)
  recurrence_pattern?: string; // JSON string defining recurrence rules
  original_task_id?: string; // Links to template for recurring instances
  tags?: Tag[]; // Associated tags
}

export interface RecurrencePattern {
  type: 'daily' | 'weekly' | 'monthly' | 'custom';
  interval: number;
  days_of_week?: number[]; // 0 = Sunday, 1 = Monday, ..., 6 = Saturday
  day_of_month?: number; // For monthly recurrence (1-31)
  end_date?: string; // ISO date string for end date
  occurrences?: number; // Number of occurrences before stopping
}

export interface Reminder {
  id: string; // UUID identifier
  task_id: string; // Foreign key to Task
  reminder_time: string; // ISO date string for when the reminder should be sent
  reminder_type: 'email' | 'browser_notification' | 'both'; // Type of reminder to send
  user_id: string; // Foreign key to User
  created_at: string; // ISO date string
  sent_at?: string; // ISO date string when the reminder was sent (null if not sent yet)
}

export interface CreateReminderRequest {
  task_id: string; // Task ID to remind about
  reminder_time: string; // ISO date string for reminder time
  reminder_type?: 'email' | 'browser_notification' | 'both'; // Type of reminder (default: browser_notification)
}

export interface UpdateReminderRequest {
  reminder_time?: string; // ISO date string for new reminder time
  reminder_type?: 'email' | 'browser_notification' | 'both'; // New type of reminder
  sent_at?: string; // ISO date string when reminder was sent
}

// Tag Interface
export interface Tag {
  id: string; // UUID identifier
  name: string; // Tag name (1-50 characters)
  color?: string; // Hex color code for visual representation
  user_id: string; // Foreign key to User
  created_at: string; // ISO date string
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
  priority?: string; // Priority level (high, medium, low)
  due_date?: string; // Due date string (ISO format)
  recurrence_pattern?: string; // JSON string defining recurrence rules
  tag_ids?: string[]; // Array of tag IDs to associate
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: string; // Priority level (high, medium, low)
  due_date?: string; // Due date string (ISO format)
  recurrence_pattern?: string; // JSON string defining recurrence rules
  tag_ids?: string[]; // Array of tag IDs to associate
  version: number; // Required for optimistic locking
}

// Tag Request Types
export interface CreateTagRequest {
  name: string;
  color?: string; // Hex color code
}

export interface UpdateTagRequest {
  name?: string;
  color?: string; // Hex color code
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
  onTaskCreated?: (task: Task) => void;
  onTaskUpdated?: (task: Task) => void;
  onCancel?: () => void;
  initialValues?: Partial<CreateTaskRequest>;
  availableTags?: Tag[]; // Available tags for selection
  taskId?: string; // For updates
}

export interface TaskListProps {
  tasks?: Task[];
  loading?: boolean;
  onToggle: (taskId: string, version: number) => void;
  onUpdate: (taskId: string, updates: Partial<Task>) => void;
  onDelete: (taskId: string) => void;
  availableTags?: Tag[];
  emptyMessage?: string;
}