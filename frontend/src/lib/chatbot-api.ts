/**
 * API client for chatbot functionality
 */

interface ChatRequest {
  message: string;
  conversation_id?: number;
}

interface ChatResponse {
  message: string;
  response?: string;
  success?: boolean;
  action?: string;
  task_id?: string;
  conversation_id?: number;
  tool_calls?: unknown[];
}

import { jwtDecode } from 'jwt-decode';

/**
 * Extract user ID from JWT token
 */
function getUserIdFromToken(token: string): string | null {
  try {
    const decoded: any = jwtDecode(token);
    return decoded.sub || null;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
}

/**
 * Process natural language commands for the chatbot
 */
export async function processNlpCommand(command: string, authToken: string | null): Promise<ChatResponse> {
  if (!authToken) {
    throw new Error('Authentication required');
  }

  const userId = getUserIdFromToken(authToken);
  if (!userId) {
    throw new Error('Invalid authentication token');
  }

  try {
    // NEXT_PUBLIC_API_URL may include /api suffix, so we need the base URL
    let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    // Remove trailing /api if present to avoid double /api/api/
    API_BASE_URL = API_BASE_URL.replace(/\/api\/?$/, '');
    const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authToken}`
      },
      body: JSON.stringify({
        message: command
      })
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    // Normalize response format for the chatbot widget
    return {
      message: data.response || data.message || 'No response',
      response: data.response,
      success: true,
      conversation_id: data.conversation_id,
      tool_calls: data.tool_calls
    };
  } catch (error) {
    console.error('Error processing chat command:', error);
    throw error;
  }
}