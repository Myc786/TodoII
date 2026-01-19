/**
 * API client for chatbot functionality
 */

interface ChatRequest {
  message: string;
  user_id?: string;
  intent?: string;
}

interface ChatResponse {
  message: string;
  success: boolean;
  action?: string;
  task_id?: string;
}

/**
 * Process natural language commands for the chatbot
 */
export async function processNlpCommand(command: string, authToken: string | null): Promise<ChatResponse> {
  if (!authToken) {
    throw new Error('Authentication required');
  }

  try {
    const response = await fetch('http://localhost:8000/api/chat', {
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

    const data: ChatResponse = await response.json();
    return data;
  } catch (error) {
    console.error('Error processing chat command:', error);
    throw error;
  }
}