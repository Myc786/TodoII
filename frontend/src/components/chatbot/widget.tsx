'use client';

import { useState, useEffect, useRef } from 'react';
import { ChatKitWrapper } from './chatkit-wrapper';
import { Button } from '@/components/ui/button';
import { MessageCircle, X } from 'lucide-react';
import { useTheme } from 'next-themes';

interface ChatWidgetProps {
  userId?: string;
  authToken?: string;
}

export function ChatWidget({ userId, authToken }: ChatWidgetProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(true);
  const { theme } = useTheme();
  const widgetRef = useRef<HTMLDivElement>(null);

  // Close chat when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (widgetRef.current && !widgetRef.current.contains(event.target as Node)) {
        if (isOpen) {
          setIsOpen(false);
        }
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // Handle visibility based on viewport
  useEffect(() => {
    const handleResize = () => {
      setIsVisible(window.innerWidth >= 768); // Hide on mobile by default
    };

    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  if (!isVisible) {
    return null;
  }

  return (
    <div
      ref={widgetRef}
      className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3"
    >
      {isOpen ? (
        <div className="w-80 h-96 bg-background border rounded-lg shadow-lg flex flex-col overflow-hidden">
          <div className="flex justify-between items-center p-3 bg-primary text-primary-foreground border-b">
            <span className="font-medium">AI Todo Assistant</span>
            <Button
              variant="ghost"
              size="sm"
              className="text-primary-foreground hover:text-primary-foreground hover:bg-primary/10"
              onClick={() => setIsOpen(false)}
            >
              <X className="h-4 w-4" />
            </Button>
          </div>
          <ChatKitWrapper userId={userId} authToken={authToken} />
        </div>
      ) : null}

      <Button
        variant="default"
        size="lg"
        className={`rounded-full w-14 h-14 shadow-lg flex items-center justify-center ${
          theme === 'dark' ? 'bg-primary hover:bg-primary/90' : 'bg-primary hover:bg-primary/90'
        }`}
        onClick={() => setIsOpen(!isOpen)}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        <MessageCircle className="h-6 w-6" />
      </Button>
    </div>
  );
}