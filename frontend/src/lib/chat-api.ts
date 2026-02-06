/**
 * Chat API client functions for communicating with backend chat endpoint.
 */

import { ChatRequest, ChatResponse, Message } from '@/types/chat';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Send a chat message to the backend.
 *
 * @param userId - User ID from authentication
 * @param message - User message text
 * @param conversationId - Optional conversation ID for continuing conversation
 * @param token - JWT authentication token
 * @returns Chat response with conversation_id, response, and tool_calls
 * @throws Error if request fails
 */
export async function sendMessage(
  userId: number,
  message: string,
  conversationId: number | null,
  token: string
): Promise<ChatResponse> {
  const request: ChatRequest = {
    message,
    ...(conversationId && { conversation_id: conversationId })
  };

  const response = await fetch(`${API_BASE_URL}/api/${userId}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(request)
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: 'Failed to send message'
    }));
    throw new Error(error.detail || 'Failed to send message');
  }

  return response.json();
}

/**
 * Load conversation history (for future use - User Story 5).
 *
 * @param userId - User ID from authentication
 * @param conversationId - Conversation ID to load
 * @param token - JWT authentication token
 * @returns Array of messages
 * @throws Error if request fails
 */
export async function loadHistory(
  userId: number,
  conversationId: number,
  token: string
): Promise<Message[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/${userId}/conversations/${conversationId}/messages`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      detail: 'Failed to load conversation history'
    }));
    throw new Error(error.detail || 'Failed to load history');
  }

  return response.json();
}

/**
 * List user's conversations (for future use - User Story 5).
 *
 * @param userId - User ID from authentication
 * @param token - JWT authentication token
 * @returns Array of conversations
 * @throws Error if request fails
 */
export async function listConversations(
  userId: number,
  token: string
): Promise<any[]> {
  const response = await fetch(
    `${API_BASE_URL}/api/${userId}/conversations`,
    {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    }
  );

  if (!response.ok) {
    throw new Error('Failed to load conversations');
  }

  return response.json();
}
