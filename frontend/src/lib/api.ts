import { Task, CreateTaskRequest, UpdateTaskRequest, ToggleTaskRequest, ApiResponse } from './types';

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Helper function to get auth headers
const getAuthHeaders = (): HeadersInit => {
  // With Better Auth, tokens are handled automatically by the client
  // We'll still include the Authorization header for direct API calls
  const token = localStorage.getItem('access_token') || localStorage.getItem('token');
  return {
    'Content-Type': 'application/json',
    ...(token && { 'Authorization': `Bearer ${token}` })
  };
};

// API Client Interface
export const apiClient = {
  // GET /tasks - Fetch all tasks for the authenticated user
  getTasks: async (): Promise<ApiResponse<Task[]>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (response.status === 401) {
        // Redirect to login if unauthorized
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized - redirecting to login');
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const tasks: Task[] = await response.json();
      return { data: tasks, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // POST /tasks - Create a new task
  createTask: async (taskData: CreateTaskRequest): Promise<ApiResponse<Task>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(taskData),
      });

      if (response.status === 401) {
        // Redirect to login if unauthorized
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized - redirecting to login');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const task: Task = await response.json();
      return { data: task, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // GET /tasks/{task_id} - Get a specific task
  getTaskById: async (taskId: string): Promise<ApiResponse<Task>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/`, {
        method: 'GET',
        headers: getAuthHeaders(),
      });

      if (response.status === 401) {
        // Redirect to login if unauthorized
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized - redirecting to login');
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const task: Task = await response.json();
      return { data: task, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // PUT /tasks/{task_id} - Update a specific task
  updateTask: async (taskId: string, taskData: UpdateTaskRequest): Promise<ApiResponse<Task>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(taskData),
      });

      if (response.status === 401) {
        // Redirect to login if unauthorized
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized - redirecting to login');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const task: Task = await response.json();
      return { data: task, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // PATCH /tasks/{task_id}/toggle - Toggle the completion status of a task
  toggleTaskCompletion: async (taskId: string, toggleData: ToggleTaskRequest): Promise<ApiResponse<Task>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/toggle/`, {
        method: 'PATCH',
        headers: getAuthHeaders(),
        body: JSON.stringify(toggleData),
      });

      if (response.status === 401) {
        // Redirect to login if unauthorized
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized - redirecting to login');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const task: Task = await response.json();
      return { data: task, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // DELETE /tasks/{task_id} - Delete a specific task
  deleteTask: async (taskId: string): Promise<ApiResponse<void>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/`, {
        method: 'DELETE',
        headers: getAuthHeaders(),
      });

      if (response.status === 401) {
        // Redirect to login if unauthorized
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized - redirecting to login');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return { success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // GET /health - Check API health status
  healthCheck: async (): Promise<ApiResponse<{ status: string; environment: string }>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const health = await response.json();
      return { data: health, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },
};

export default apiClient;