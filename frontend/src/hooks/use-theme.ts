import { useTheme as useNextTheme } from 'next-themes';

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