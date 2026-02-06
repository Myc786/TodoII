/**
 * TypeScript types for AI chatbot feature.
 */

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  tool_calls?: ToolCall[];
  created_at?: string;
}

export interface ToolCall {
  tool: string;
  arguments: Record<string, any>;
  result: Record<string, any>;
}

export interface Conversation {
  id: number;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatResponse {
  conversation_id: number;
  response: string;
  tool_calls: ToolCall[];
}
