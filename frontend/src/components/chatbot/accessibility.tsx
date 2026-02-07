/**
 * Accessibility utilities for the Todo Chatbot Extension
 */

import { useEffect, useState, KeyboardEvent } from 'react';

// ARIA live region for announcements
export function AriaLiveAnnouncer({ children }: { children: string }) {
  return (
    <div
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
      role="status"
    >
      {children}
    </div>
  );
}

// Focus trap for modal dialogs
export function useFocusTrap(ref: React.RefObject<HTMLElement>) {
  useEffect(() => {
    if (!ref.current) return;

    const focusableElements = ref.current.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    if (focusableElements.length === 0) return;

    const firstElement = focusableElements[0] as HTMLElement;
    const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key !== 'Tab') return;

      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          lastElement.focus();
          e.preventDefault();
        }
      } else {
        if (document.activeElement === lastElement) {
          firstElement.focus();
          e.preventDefault();
        }
      }
    };

    firstElement.focus();

    const element = ref.current;
    element.addEventListener('keydown', handleKeyDown as any);

    return () => {
      element.removeEventListener('keydown', handleKeyDown as any);
    };
  }, [ref]);
}

// Keyboard shortcuts for chat
export function useChatKeyboardShortcuts(
  sendMessage: (message: string) => void,
  currentInput: string,
  setCurrentInput: (input: string) => void
) {
  useEffect(() => {
    const handleGlobalKeyDown = (e: KeyboardEvent) => {
      // Focus chat input with Ctrl/Cmd + K
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        const inputElement = document.querySelector('#chat-input') as HTMLInputElement;
        if (inputElement) {
          inputElement.focus();
        }
      }

      // Send message with Ctrl/Cmd + Enter
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (currentInput.trim()) {
          sendMessage(currentInput);
          setCurrentInput('');
        }
      }
    };

    document.addEventListener('keydown', handleGlobalKeyDown as any);
    return () => document.removeEventListener('keydown', handleGlobalKeyDown as any);
  }, [sendMessage, currentInput, setCurrentInput]);
}

// Screen reader announcement hook
export function useScreenReaderAnnouncement() {
  const [announcement, setAnnouncement] = useState('');

  useEffect(() => {
    if (announcement) {
      // Clear announcement after it's been announced
      const timer = setTimeout(() => {
        setAnnouncement('');
      }, 1000);

      return () => clearTimeout(timer);
    }
  }, [announcement]);

  return { announcement, setAnnouncement };
}

// Accessible chat message component
interface AccessibleMessageProps {
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  id: string;
}

export function AccessibleMessage({ content, role, timestamp, id }: AccessibleMessageProps) {
  const messageRoleLabel = role === 'user' ? 'Sent by you' : 'Received from AI assistant';
  const timeFormatted = timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  return (
    <div
      id={`message-${id}`}
      className={`flex ${role === 'user' ? 'justify-end' : 'justify-start'}`}
      role="log"
      aria-label={`${messageRoleLabel} at ${timeFormatted}`}
    >
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2 text-sm ${
          role === 'user'
            ? 'bg-blue-500 text-white rounded-br-sm'
            : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-bl-sm'
        }`}
        tabIndex={0}
        aria-describedby={`message-${id}-meta`}
      >
        <div>{content}</div>
        <div
          id={`message-${id}-meta`}
          className="sr-only"
        >
          {messageRoleLabel} at {timeFormatted}
        </div>
      </div>
    </div>
  );
}

// Accessible chat input component
interface AccessibleChatInputProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  disabled?: boolean;
}

export function AccessibleChatInput({ value, onChange, onSubmit, disabled }: AccessibleChatInputProps) {
  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      if (value.trim() && !disabled) {
        onSubmit();
      }
    }
  };

  return (
    <div className="relative w-full">
      <textarea
        id="chat-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown as any}
        placeholder="Type your message..."
        disabled={disabled}
        rows={1}
        className="w-full px-3 py-2 pr-10 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-background text-foreground resize-none"
        aria-label="Type your message to the AI assistant"
        aria-disabled={disabled}
        aria-required
      />
      <button
        onClick={onSubmit}
        disabled={!value.trim() || disabled}
        className="absolute right-2 bottom-2 px-3 py-1 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed text-sm"
        aria-label="Send message"
        aria-disabled={!value.trim() || disabled}
      >
        Send
      </button>
    </div>
  );
}