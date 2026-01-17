# Theme System Documentation

## Overview
The application includes a dynamic theme system that supports light mode, dark mode, and system preference detection. The theme system is built using `next-themes` and integrates seamlessly with Tailwind CSS.

## Features
- Light/Dark theme switching
- System preference detection (respects user's OS-level theme setting)
- Theme persistence across page reloads
- Smooth theme transitions
- Accessible design with reduced motion support

## Implementation Details

### Context Provider
The theme system is implemented using a React Context Provider pattern:

```tsx
// In src/app/layout.tsx
import { ThemeProvider } from '@/contexts/theme-context';

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <AuthProvider>
          <ThemeProvider>
            {children}
          </ThemeProvider>
        </AuthProvider>
      </body>
    </html>
  );
}
```

### Custom Hook
Use the `useTheme` hook to access theme functionality:

```tsx
import { useTheme } from '@/hooks/use-theme';

export function MyComponent() {
  const { theme, resolvedTheme, toggleTheme, setTheme } = useTheme();

  return (
    <div>
      <p>Current theme: {theme}</p>
      <p>Resolved theme: {resolvedTheme}</p>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
}
```

### Theme Toggle Component
The theme toggle component provides a UI element for users to switch themes:

```tsx
import { ThemeToggle } from '@/components/ui/theme-toggle';

// Use in your header or anywhere in the app
function Header() {
  return (
    <header>
      {/* other header content */}
      <ThemeToggle />
    </header>
  );
}
```

## CSS Variables
The theme system uses CSS variables defined in `src/app/globals.css`:

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;
  /* ... other variables */
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;
  /* ... other variables */
}
```

## 3D Effects and Visual Enhancements
The system includes enhanced 3D visual effects that work with both themes:

- `card-3d`: Adds depth and hover effects to card components
- `button-3d`: Adds shine and press effects to buttons
- `checkbox-3d`: Adds scaling effects to checkboxes
- `text-glow`: Subtle text glow effect

## Responsive and Accessible Design
- Respects `prefers-reduced-motion` setting
- Optimized for touch devices
- Proper ARIA labels for screen readers
- Semantic HTML structure

## Best Practices
1. Always wrap your application with `<ThemeProvider>` at the root level
2. Use the `useTheme` hook to access theme state in components
3. Leverage Tailwind's `dark:` prefix for theme-specific styling
4. Include proper ARIA labels for interactive elements
5. Test with reduced motion settings enabled