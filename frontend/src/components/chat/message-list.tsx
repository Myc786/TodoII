/**
 * MessageList component for displaying conversation messages.
 */

'use client';

import { useEffect, useRef } from 'react';
import { Message } from '@/types/chat';

interface MessageListProps {
  messages: Message[];
}

/**
 * Format message content with enhanced styling for task lists.
 * Detects task list patterns and applies formatting.
 */
function formatMessageContent(content: string, role: string) {
  // For assistant messages, enhance task list formatting
  if (role === 'assistant') {
    // Detect numbered lists (1., 2., 3., etc.)
    const hasNumberedList = /^\d+\.\s+/m.test(content);
    // Detect bullet points (•, -, *, etc.)
    const hasBulletPoints = /^[•\-\*]\s+/m.test(content);

    if (hasNumberedList || hasBulletPoints) {
      const lines = content.split('\n');
      return (
        <div className="space-y-1">
          {lines.map((line, idx) => {
            // Match task lines with status indicators
            const taskMatch = line.match(/^(\d+\.|[•\-\*])\s+(.+?)\s*\(?(pending|completed)?\)?.*?(Task #\d+)?$/i);

            if (taskMatch) {
              const [, bullet, title, status, taskId] = taskMatch;
              return (
                <div key={idx} className="flex items-start gap-2 py-1">
                  <span className="font-mono text-sm opacity-70">{bullet}</span>
                  <div className="flex-1">
                    <span className="font-medium">{title.trim()}</span>
                    {status && (
                      <span
                        className={`ml-2 text-xs px-2 py-0.5 rounded ${
                          status.toLowerCase() === 'completed'
                            ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
                            : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-300'
                        }`}
                      >
                        {status}
                      </span>
                    )}
                    {taskId && (
                      <span className="ml-2 text-xs opacity-60 font-mono">
                        {taskId}
                      </span>
                    )}
                  </div>
                </div>
              );
            }

            // Regular line (e.g., "You have 3 tasks:")
            return (
              <div key={idx} className={line.trim() ? 'py-0.5' : ''}>
                {line}
              </div>
            );
          })}
        </div>
      );
    }
  }

  // Default: return content as-is
  return content;
}

export function MessageList({ messages }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="text-center text-gray-500 dark:text-gray-400">
          <svg
            className="mx-auto h-12 w-12 mb-4"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
            />
          </svg>
          <p className="text-lg font-medium">Start a conversation</p>
          <p className="text-sm mt-1">
            Try: "Add a task to buy groceries" or "Show me my tasks"
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-[70%] rounded-lg px-4 py-2 ${
              message.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-gray-200 dark:bg-gray-700 text-gray-900 dark:text-gray-100'
            }`}
          >
            <div className="whitespace-pre-wrap break-words">
              {formatMessageContent(message.content, message.role)}
            </div>

            {/* Display tool calls if present */}
            {message.tool_calls && message.tool_calls.length > 0 && (
              <div className="mt-2 pt-2 border-t border-gray-300 dark:border-gray-600 text-xs">
                <div className="flex flex-wrap items-center gap-2">
                  {message.tool_calls.map((call, idx) => {
                    const isListTool = call.tool === 'list_tasks';
                    const isAddTool = call.tool === 'add_task';
                    const isCompleteTool = call.tool === 'complete_task';

                    return (
                      <div
                        key={idx}
                        className={`flex items-center gap-1 px-2 py-1 rounded text-xs ${
                          isListTool
                            ? 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-300'
                            : isAddTool
                            ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300'
                            : isCompleteTool
                            ? 'bg-purple-100 text-purple-700 dark:bg-purple-900/30 dark:text-purple-300'
                            : 'bg-gray-100 text-gray-700 dark:bg-gray-600 dark:text-gray-300'
                        }`}
                      >
                        <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20">
                          <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                        </svg>
                        <span className="font-medium">
                          {call.tool.replace(/_/g, ' ')}
                        </span>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {message.created_at && (
              <div className="text-xs mt-1 opacity-70">
                {new Date(message.created_at).toLocaleTimeString()}
              </div>
            )}
          </div>
        </div>
      ))}
      <div ref={messagesEndRef} />
    </div>
  );
}
