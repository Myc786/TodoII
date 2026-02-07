/**
 * ChatInterface component - Main chat interface integrating MessageList and ChatInput.
 */

'use client';

import { useState, useEffect } from 'react';
import { Message, ChatResponse } from '@/types/chat';
import { MessageList } from './message-list';
import { ChatInput } from './chat-input';
import { sendMessage } from '@/lib/chat-api';
import { conversationStorage } from '@/lib/conversation-storage';

interface ChatInterfaceProps {
  userId: string;
  token: string;
}

export function ChatInterface({ userId, token }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load conversation ID from localStorage on mount
  useEffect(() => {
    const storedConversationId = conversationStorage.getConversationId();
    if (storedConversationId) {
      setConversationId(storedConversationId);
      // TODO: Load conversation history (User Story 5)
    }
  }, []);

  const handleSendMessage = async (messageText: string) => {
    setError(null);
    setLoading(true);

    // Add user message to UI immediately (optimistic update)
    const userMessage: Message = {
      role: 'user',
      content: messageText
    };
    setMessages((prev) => [...prev, userMessage]);

    try {
      // Send message to backend
      const response: ChatResponse = await sendMessage(
        userId,
        messageText,
        conversationId,
        token
      );

      // Update conversation ID if new conversation
      if (!conversationId || response.conversation_id !== conversationId) {
        setConversationId(response.conversation_id);
        conversationStorage.setConversationId(response.conversation_id);
      }

      // Add assistant response to messages
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        tool_calls: response.tool_calls
      };
      setMessages((prev) => [...prev, assistantMessage]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to send message');

      // Remove optimistic user message on error
      setMessages((prev) => prev.slice(0, -1));
    } finally {
      setLoading(false);
    }
  };

  const handleNewConversation = () => {
    setMessages([]);
    setConversationId(null);
    conversationStorage.clearConversationId();
    setError(null);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="border-b border-gray-200 dark:border-gray-700 p-4 flex justify-between items-center">
        <div>
          <h1 className="text-xl font-semibold text-gray-900 dark:text-gray-100">
            AI Task Assistant
          </h1>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Manage your tasks with natural language
          </p>
        </div>
        <button
          onClick={handleNewConversation}
          className="px-4 py-2 text-sm bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
        >
          New Conversation
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 m-4">
          <div className="flex items-center">
            <svg
              className="h-5 w-5 text-red-500 mr-2"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clipRule="evenodd"
              />
            </svg>
            <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
          </div>
        </div>
      )}

      {/* Messages */}
      <MessageList messages={messages} />

      {/* Input */}
      <ChatInput onSendMessage={handleSendMessage} loading={loading} />
    </div>
  );
}
