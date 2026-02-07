'use client';

import { useState, useEffect, useCallback } from 'react';
import { useTheme } from 'next-themes';
import { useChatAuth } from '@/contexts/chat-auth-context';
import { processNlpCommand } from '@/lib/chatbot-api'; // This would be our API function
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';

interface ChatKitWrapperProps {
  userId?: string;
  authToken?: string;
}

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  createdAt: Date;
}

export function ChatKitWrapper({ userId, authToken: propAuthToken }: ChatKitWrapperProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { theme } = useTheme();
  const { getAuthToken } = useChatAuth();

  // Get auth token from context if not provided as prop
  const authToken = propAuthToken || getAuthToken();

  // Load initial messages if needed
  useEffect(() => {
    // Initialize with a welcome message
    setMessages([
      {
        id: 'welcome',
        content: 'Hello! I\'m your AI Todo Assistant. How can I help you today?',
        role: 'assistant',
        createdAt: new Date(),
      }
    ]);
  }, []);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputValue.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputValue.trim(),
      role: 'user',
      createdAt: new Date(),
    };

    // Add user message to the chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Get the auth token from prop or context
      const token = authToken || getAuthToken();

      if (!token) {
        throw new Error('Authentication token not available');
      }

      // Process the command via the chatbot API
      const response = await processNlpCommand(inputValue.trim(), token);

      // Trigger a refresh of the task list if tools were called
      if (response.tool_calls && response.tool_calls.length > 0) {
        window.dispatchEvent(new CustomEvent('task-updated'));
      }

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: response.message || "I processed your command successfully!",
        role: 'assistant',
        createdAt: new Date(),
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('Error processing command:', error);

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}. Please try again.`,
        role: 'assistant',
        createdAt: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, [inputValue, isLoading, authToken, getAuthToken]);

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  return (
    <div className={`flex flex-col h-full bg-${theme === 'dark' ? 'gray-900' : 'white'} text-${theme === 'dark' ? 'white' : 'black'}`}>
      {/* Messages Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${message.role === 'user'
                ? 'bg-blue-500 text-white rounded-br-sm'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-sm'
                }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-2xl px-4 py-2 text-sm rounded-bl-sm">
              <div className="flex items-center">
                <div className="w-2 h-2 bg-gray-500 rounded-full mr-1 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full mr-1 animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                <span className="ml-2">AI is thinking...</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t p-3 bg-background">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <Input
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
            disabled={isLoading}
            className="flex-1"
          />
          <Button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="shrink-0"
          >
            Send
          </Button>
        </form>
      </div>
    </div>
  );
}