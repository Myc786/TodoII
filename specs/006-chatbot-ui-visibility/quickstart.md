# Quickstart Guide: AI-Powered Todo Chatbot Integration

## Overview
This guide provides instructions for integrating the AI-powered chatbot UI into the Todo application.

## Prerequisites
- Node.js 18+ installed
- Python 3.9+ installed (for backend)
- Next.js 14+ project
- Existing authentication system with JWT tokens

## Installation Steps

### 1. Verify Existing Components
Ensure the following components are available:
- `frontend/src/components/chatbot/widget.tsx` (ChatWidget)
- `frontend/src/contexts/chat-auth-context.tsx` (ChatAuthProvider)
- Authentication system with `useAuth` hook

### 2. Update Root Layout
Modify `frontend/src/app/layout.tsx` to include the ChatWidget:

```tsx
import { ChatWidget } from '@/components/chatbot/widget';

// Inside the body of the RootLayout component
return (
  <html lang="en" suppressHydrationWarning>
    <body className={inter.className}>
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        <AuthWrapper>
          {children}
          <ChatWidget /> {/* Add this line to render the chatbot */}
        </AuthWrapper>
      </ThemeProvider>
    </body>
  </html>
);
```

### 3. Connect Authentication
The ChatWidget should automatically connect to the authentication context. Ensure the AuthWrapper provides the necessary authentication state.

### 4. Environment Configuration
Add any necessary environment variables to `.env.local`:
```
NEXT_PUBLIC_CHAT_API_URL=http://localhost:8000/api/chat
NEXT_PUBLIC_ENABLE_CHATBOT=true
```

## Testing the Integration

### 1. Start the Application
```bash
# Start the backend
cd backend
uvicorn src.main:app --reload

# Start the frontend
cd frontend
npm run dev
```

### 2. Verify Functionality
- Navigate to the application in your browser
- Log in with valid credentials
- Verify the chatbot widget appears as a floating button in the bottom-right corner
- Click the chatbot button to expand the chat panel
- Test sending messages and receiving responses

### 3. Test Different Scenarios
- Test with authenticated and unauthenticated users
- Verify behavior in light and dark themes
- Test on different screen sizes (ensure it hides on mobile as expected)
- Test error handling scenarios

## Troubleshooting

### Chatbot Widget Not Appearing
- Verify the ChatWidget is added to the layout
- Check that the user is properly authenticated
- Verify that the screen width is ≥768px (chatbot hides on smaller screens)

### Authentication Issues
- Ensure JWT token is properly stored in localStorage as 'access_token'
- Verify the ChatAuthProvider is properly wrapped around the application
- Check that the auth context is accessible to the ChatWidget

### Theme Inconsistencies
- Verify that the theme context is properly provided to the ChatWidget
- Check that Tailwind CSS classes are applied correctly for both themes