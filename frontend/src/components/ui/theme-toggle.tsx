'use client';

import { Moon, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';

import { Button } from '@/components/ui/button';

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  const toggleTheme = () => {
    if (theme === 'dark') {
      setTheme('light');
    } else if (theme === 'light') {
      setTheme('system');
    } else {
      setTheme('dark');
    }
  };

  return (
    <Button
      variant="ghost"
      size="icon"
      aria-label="Theme toggle"
      className="button-3d relative overflow-hidden"
      onClick={toggleTheme}
    >
      {/* Animated background */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-purple-500 opacity-0 hover:opacity-10 rounded-full transition-opacity duration-300" />

      <div className="relative w-5 h-5">
        <Sun className="absolute h-5 w-5 transition-all duration-300 rotate-0 scale-100 dark:-rotate-90 dark:scale-0" />
        <Moon className="absolute h-5 w-5 transition-all duration-300 rotate-90 scale-0 dark:rotate-0 dark:scale-100" />
      </div>

      {/* Theme indicator */}
      <span className="sr-only">
        {theme === 'dark' ? 'Switch to light mode' :
         theme === 'light' ? 'Switch to system mode' : 'Switch to dark mode'}
      </span>
    </Button>
  );
}