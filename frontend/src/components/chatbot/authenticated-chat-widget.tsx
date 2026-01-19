'use client';

import { useAuth } from '@/hooks/use-auth';
import { ChatWidget } from './widget';
import { Component, ReactNode } from 'react';
import { ChatAuthProvider } from '@/contexts/chat-auth-context';

// Error Boundary component to catch errors in the chat widget
class ChatWidgetErrorBoundary extends Component<{
  children: ReactNode;
  fallback: ReactNode;
}> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('ChatWidget error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback;
    }

    return this.props.children;
  }
}

// Fallback UI for when the chat widget fails
function ChatWidgetFallback() {
  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
        <strong className="font-bold">Chat Error! </strong>
        <span className="block sm:inline">There was an issue loading the chatbot. Please refresh the page.</span>
      </div>
    </div>
  );
}

export function AuthenticatedChatWidget() {
  const { user, isAuthenticated } = useAuth();

  // Only render the chat widget if the user is authenticated
  if (!isAuthenticated) {
    return null;
  }

  // Pass user ID and token to the chat widget with error boundary protection
  // Wrap with ChatAuthProvider to provide chat-specific authentication context
  return (
    <ChatWidgetErrorBoundary fallback={<ChatWidgetFallback />}>
      <ChatAuthProvider>
        <ChatWidget userId={user?.id} authToken={localStorage.getItem('access_token') || undefined} />
      </ChatAuthProvider>
    </ChatWidgetErrorBoundary>
  );
}