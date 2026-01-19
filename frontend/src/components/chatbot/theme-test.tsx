/**
 * Theme integration test for the Todo Chatbot Extension
 * This component verifies that the chat UI works correctly with light/dark themes
 */

import { useEffect, useState } from 'react';
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import { ChatContainer } from './container';

export function ThemeIntegrationTest() {
  const { theme, setTheme, systemTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  // useEffect only runs on the client, so we can safely set mounted to true
  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    // Don't render anything until after hydration
    return <div>Loading...</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-bold">Theme Integration Test</h1>

      <div className="flex gap-4 items-center p-4 border rounded-lg bg-muted">
        <p className="font-medium">Current theme: <span className="font-mono">{theme}</span></p>
        <div className="flex gap-2">
          <Button onClick={() => setTheme('light')}>Light</Button>
          <Button onClick={() => setTheme('dark')}>Dark</Button>
          <Button onClick={() => setTheme('system')}>System ({systemTheme})</Button>
        </div>
      </div>

      <div className="p-4 border rounded-lg bg-muted">
        <h2 className="text-xl font-semibold mb-4">Chat Container Test</h2>
        <p className="mb-4 text-muted-foreground">
          The chat container below should adapt to the selected theme.
          Test by expanding/collapsing the chat widget and verifying that all UI elements
          (backgrounds, text colors, borders) update appropriately.
        </p>

        {/* Render the chat container to test theme integration */}
        <div className="relative h-96 border-2 border-dashed border-gray-300 rounded-lg p-4 flex items-center justify-center bg-background">
          <p className="text-center text-muted-foreground">
            Chat container will appear here when expanded
          </p>

          {/* Position the chat container in the bottom right */}
          <div className="absolute bottom-4 right-4">
            <ChatContainer />
          </div>
        </div>
      </div>

      <div className="p-4 border rounded-lg bg-muted">
        <h2 className="text-xl font-semibold mb-2">Theme Elements Test</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 border rounded-lg bg-background">
            <h3 className="font-medium mb-2">Background</h3>
            <p className="text-sm text-muted-foreground">This should match the theme background</p>
          </div>
          <div className="p-4 border rounded-lg bg-secondary">
            <h3 className="font-medium mb-2">Secondary Background</h3>
            <p className="text-sm text-muted-foreground">This should adapt to the theme</p>
          </div>
          <div className="p-4 border rounded-lg bg-muted">
            <h3 className="font-medium mb-2">Muted Background</h3>
            <p className="text-sm text-muted-foreground">This should adapt to the theme</p>
          </div>
        </div>
      </div>

      <div className="p-4 border rounded-lg bg-muted">
        <h2 className="text-xl font-semibold mb-2">Text Colors Test</h2>
        <div className="space-y-2">
          <p className="text-foreground">Primary text - should be readable in both themes</p>
          <p className="text-muted-foreground">Muted text - should be readable but less prominent</p>
          <p className="text-destructive">Destructive text - should be clearly visible</p>
        </div>
      </div>
    </div>
  );
}