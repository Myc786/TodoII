'use client';

import { createContext, useContext, ReactNode } from 'react';
import { ThemeProvider as NextThemesProvider, useTheme as useNextTheme } from 'next-themes';

interface ThemeContextType {
  theme: 'light' | 'dark' | 'system';
  resolvedTheme: 'light' | 'dark';
  toggleTheme: () => void;
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  return (
    <NextThemesProvider attribute="class" defaultTheme="system">
      {children}
    </NextThemesProvider>
  );
};

export const useTheme = () => {
  const context = useNextTheme();
  const toggleTheme = () => {
    if (context.theme === 'light') {
      context.setTheme('dark');
    } else {
      context.setTheme('light');
    }
  };

  return {
    theme: context.theme as 'light' | 'dark' | 'system',
    resolvedTheme: context.resolvedTheme as 'light' | 'dark',
    toggleTheme,
    setTheme: context.setTheme
  };
};