'use client';

import { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { ChatKitWrapper } from './chatkit-wrapper';
import { MessageCircle, X } from 'lucide-react';
import { useTheme } from 'next-themes';

interface ChatContainerProps {
  userId?: string;
  authToken?: string;
}

export function ChatContainer({ userId, authToken }: ChatContainerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(true);
  const { theme } = useTheme();
  const containerRef = useRef<HTMLDivElement>(null);

  // Close chat when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
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
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end gap-3">
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8, y: 20, x: 50 }}
            animate={{ opacity: 1, scale: 1, y: 0, x: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20, x: 50 }}
            transition={{
              type: "spring",
              damping: 25,
              stiffness: 300,
              duration: 0.3
            }}
            className="w-80 h-96 bg-background border rounded-lg shadow-lg flex flex-col overflow-hidden"
            ref={containerRef}
          >
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
            <div className="flex-1 overflow-hidden">
              <ChatKitWrapper userId={userId} authToken={authToken} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <motion.div
        initial={false}
        animate={{
          y: isOpen ? -100 : 0,
          rotate: isOpen ? 135 : 0
        }}
        transition={{
          type: "spring",
          damping: 20,
          stiffness: 300,
          duration: 0.3
        }}
      >
        <Button
          variant="default"
          size="lg"
          className={`rounded-full w-14 h-14 shadow-lg flex items-center justify-center ${
            theme === 'dark' ? 'bg-primary hover:bg-primary/90' : 'bg-primary hover:bg-primary/90'
          }`}
          onClick={() => setIsOpen(!isOpen)}
          aria-label={isOpen ? "Close chat" : "Open chat"}
          ref={undefined} // Fix for motion component
        >
          <motion.span
            animate={{ rotate: isOpen ? 90 : 0 }}
            transition={{ duration: 0.2 }}
          >
            {isOpen ? (
              <X className="h-6 w-6" />
            ) : (
              <MessageCircle className="h-6 w-6" />
            )}
          </motion.span>
        </Button>
      </motion.div>
    </div>
  );
}