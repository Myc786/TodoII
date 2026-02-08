import { Task, Tag, CreateTaskRequest, UpdateTaskRequest, ToggleTaskRequest, CreateTagRequest, UpdateTagRequest, ApiResponse, Reminder, CreateReminderRequest } from './types';

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

/**
 * IMPORTANT: Trailing Slash Rules for Hugging Face Spaces
 *
 * To avoid HTTP 307 redirects that drop Authorization headers:
 * - Collection endpoints (list, create): USE trailing slash
 *   Examples: GET /api/tasks/, POST /api/tasks/
 *
 * - Item endpoints (get, update, delete): NO trailing slash
 *   Examples: GET /api/tasks/{id}, PUT /api/tasks/{id}, DELETE /api/tasks/{id}
 *
 * See: TASK_ENDPOINT_INVESTIGATION.md for details
 */

// Helper function to get auth headers
const getAuthHeaders = (): HeadersInit => {
  // Attempt to get token from multiple sources
  let token = null;

  // First, try to get token from localStorage (for manual auth management)
  token = localStorage.getItem('access_token') || localStorage.getItem('token');

  // If no token found, try to get from potential global auth state
  if (!token && typeof window !== 'undefined') {
    // Check if there's a global auth state that might contain the token
    if ((window as any).__NEXTAUTH__) {
      const nextAuthState = (window as any).__NEXTAUTH__;
      if (nextAuthState && nextAuthState.session && nextAuthState.session.data && nextAuthState.session.data.accessToken) {
        token = nextAuthState.session.data.accessToken;
      }
    }
  }

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
        const errorData = await response.json().catch(() => ({ detail: `HTTP error! status: ${response.status}` }));
        console.error('Task creation failed:', errorData);
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const task: Task = await response.json();
      return { data: task, success: true };
    } catch (error) {
      console.error('Create task error:', error);
      const errorMessage = (error as Error).message;
      return { error: errorMessage === 'Failed to fetch' ? 'Network error: Please check your connection' : errorMessage, success: false };
    }
  },

  // GET /tasks/{task_id} - Get a specific task
  getTaskById: async (taskId: string): Promise<ApiResponse<Task>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
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
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
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
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}/toggle`, {
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
      const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
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

  // GET /tags - Fetch all tags for the authenticated user
  getTags: async (): Promise<ApiResponse<Tag[]>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tags/`, {
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

      const tags: Tag[] = await response.json();
      return { data: tags, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // POST /tags - Create a new tag
  createTag: async (tagData: CreateTagRequest): Promise<ApiResponse<Tag>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tags/`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(tagData),
      });

      if (response.status === 401) {
        // Redirect to login if unauthorized
        if (typeof window !== 'undefined') {
          window.location.href = '/login';
        }
        throw new Error('Unauthorized - redirecting to login');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: `HTTP error! status: ${response.status}` }));
        console.error('Tag creation failed:', errorData);
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      const tag: Tag = await response.json();
      return { data: tag, success: true };
    } catch (error) {
      console.error('Create tag error:', error);
      const errorMessage = (error as Error).message;
      return { error: errorMessage === 'Failed to fetch' ? 'Network error: Please check your connection' : errorMessage, success: false };
    }
  },

  // GET /tags/{tag_id} - Get a specific tag
  getTagById: async (tagId: string): Promise<ApiResponse<Tag>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tags/${tagId}/`, {
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

      const tag: Tag = await response.json();
      return { data: tag, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // PUT /tags/{tag_id} - Update a specific tag
  updateTag: async (tagId: string, tagData: UpdateTagRequest): Promise<ApiResponse<Tag>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tags/${tagId}/`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(tagData),
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

      const tag: Tag = await response.json();
      return { data: tag, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // DELETE /tags/{tag_id} - Delete a specific tag
  deleteTag: async (tagId: string): Promise<ApiResponse<void>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/tags/${tagId}/`, {
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
      // Health check is at root /health, not /api/health
      const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const health = await response.json();
      return { data: health, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // GET /tasks/search - Search and filter tasks
  searchAndFilterTasks: async (
    query?: string,
    status?: 'all' | 'active' | 'completed',
    priority?: string,
    tagIds?: string[],
    dueBefore?: string,
    dueAfter?: string,
    sortBy?: string,
    order?: 'asc' | 'desc',
    skip: number = 0,
    limit: number = 100
  ): Promise<ApiResponse<Task[]>> => {
    try {
      // Build query parameters
      const params = new URLSearchParams();

      if (query) params.append('q', query);
      if (status && status !== 'all') params.append('status', status);
      if (priority) params.append('priority', priority);
      if (tagIds && tagIds.length > 0) params.append('tag_ids', tagIds.join(','));
      if (dueBefore) params.append('due_before', dueBefore);
      if (dueAfter) params.append('due_after', dueAfter);
      if (sortBy) params.append('sort_by', sortBy);
      if (order) params.append('order', order);
      params.append('skip', skip.toString());
      params.append('limit', limit.toString());

      const queryString = params.toString();
      const url = queryString ? `${API_BASE_URL}/tasks/search?${queryString}` : `${API_BASE_URL}/tasks/search`;

      const response = await fetch(url, {
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

  // GET /reminders - Fetch all reminders for the authenticated user
  getReminders: async (skip: number = 0, limit: number = 100): Promise<ApiResponse<Reminder[]>> => {
    try {
      const params = new URLSearchParams();
      params.append('skip', skip.toString());
      params.append('limit', limit.toString());

      const queryString = params.toString();
      const url = queryString ? `${API_BASE_URL}/reminders?${queryString}` : `${API_BASE_URL}/reminders`;

      const response = await fetch(url, {
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

      const reminders: Reminder[] = await response.json();
      return { data: reminders, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // POST /reminders - Create a new reminder
  createReminder: async (reminderData: CreateReminderRequest): Promise<ApiResponse<Reminder>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/reminders`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify(reminderData),
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

      const reminder: Reminder = await response.json();
      return { data: reminder, success: true };
    } catch (error) {
      return { error: (error as Error).message, success: false };
    }
  },

  // DELETE /reminders/{reminder_id} - Delete a specific reminder
  deleteReminder: async (reminderId: string): Promise<ApiResponse<void>> => {
    try {
      const response = await fetch(`${API_BASE_URL}/reminders/${reminderId}`, {
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
};

export default apiClient;