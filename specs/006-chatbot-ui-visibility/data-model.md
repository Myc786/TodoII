# Data Model: AI-Powered Todo Chatbot UI

## Overview
The chatbot UI integration does not require new data models as it leverages existing authentication and theme contexts from the application.

## Existing Data Models Used

### Authentication Context
- **Source**: `useAuth` hook and `ChatAuthProvider`
- **Fields**:
  - `isAuthenticated`: boolean indicating authentication status
  - `user`: user object containing user details
  - `token`: JWT token string for API authentication

### Theme Context
- **Source**: `useTheme` hook from `next-themes`
- **Fields**:
  - `theme`: string representing current theme ('light'|'dark'|'system')
  - `setTheme`: function to change theme
  - `resolvedTheme`: string representing the resolved theme

### Chat Message Structure
- **Source**: Internal to chat components
- **Fields**:
  - `id`: string unique identifier for message
  - `content`: string content of the message
  - `role`: 'user' | 'assistant' indicating message sender
  - `createdAt`: Date timestamp of message creation

## UI State Models

### Chat Widget State
- **Component**: `ChatWidget`
- **State Fields**:
  - `isOpen`: boolean indicating if chat panel is expanded
  - `isVisible`: boolean indicating if widget should be displayed

### Chat Panel State
- **Component**: `ChatKitWrapper`
- **State Fields**:
  - `messages`: Array<Message> containing conversation history
  - `inputValue`: string current user input
  - `isLoading`: boolean indicating if response is being processed

## Integration Points

### Authentication Integration
- The chatbot UI will subscribe to authentication state changes
- Visibility will be controlled by `isAuthenticated` property
- JWT token will be accessed from localStorage for API calls

### Theme Integration
- The chatbot UI will subscribe to theme context changes
- Visual styling will automatically adapt to current theme
- Color schemes will match application's light/dark mode

## Validation Rules

### UI Display Rules
- Chatbot visible only when `isAuthenticated === true`
- Chatbot hidden on mobile devices (<768px) by default
- Chatbot respects theme context for styling

### Message Validation
- Messages must have non-empty content
- User messages require valid authentication token
- System responses validated by backend API

## Relationships

### Component Relationships
```
Root Layout -> AuthWrapper -> ChatWidget (conditional)
ChatWidget -> ChatPanel -> ChatMessages
ChatWidget -> ThemeContext (dependency)
ChatWidget -> AuthContext (dependency)
```

### Data Flow
```
Authentication State -> ChatWidget Visibility
Theme State -> ChatWidget Styling
User Input -> Message Processing -> API -> Response -> Message Display
```