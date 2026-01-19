# Specification: AI-Powered Todo Chatbot UI Visibility

## Problem Statement

The AI-powered Todo Chatbot (Phase III) is implemented logically with functional backend agents, MCP tools, and APIs, but the chatbot UI is NOT visible in the frontend. The chatbot does not appear on any page despite all backend functionality being operational.

## Root Cause Analysis

Based on investigation of the current codebase:

1. **Chatbot UI component exists but is not mounted globally** - The `ChatWidget` component exists but is not integrated into any layout or page
2. **Missing integration in main layout** - The `ChatWidget` is not included in the root layout or dashboard layout
3. **Auth state integration incomplete** - While authentication context exists, the chatbot is not connected to the auth state
4. **ChatKit provider not integrated** - The application lacks proper ChatKit provider wrapping
5. **Environment configuration** - Missing configuration to control chatbot visibility

## Objective

Ensure the chatbot UI:
- Always renders for authenticated users
- Is visible as a floating widget
- Is correctly connected to authentication and API services
- Works in both Light and Dark themes
- Appears consistently across the app

## Functional Requirements

### FR-1: Chatbot UI Placement
- **Requirement**: The chatbot must appear as a floating button positioned at the bottom-right of the screen
- **Acceptance Criteria**:
  - The chatbot button appears on all authenticated pages
  - Positioned consistently regardless of screen size (desktop)
  - Has high z-index to appear above other UI elements
- **Test**: Verify the floating button appears on dashboard, task pages, etc.

### FR-2: Authentication Integration
- **Requirement**: The chatbot must only be visible to authenticated users
- **Acceptance Criteria**:
  - Chatbot renders when user is authenticated via JWT token
  - Chatbot is hidden when user is not authenticated
  - Proper authentication context is passed to chatbot components
- **Test**: Verify chatbot appears/disappears based on auth state

### FR-3: Global Mounting Strategy
- **Requirement**: The chatbot component must be mounted at the layout level to ensure visibility across all pages
- **Acceptance Criteria**:
  - Chatbot is integrated into the main application layout
  - Component renders in a portal or fixed position that overlays content
  - Does not interfere with other UI components
- **Test**: Verify chatbot appears on all pages within the authenticated area

### FR-4: Theme Compatibility
- **Requirement**: The chatbot UI must adapt to the current theme (light/dark)
- **Acceptance Criteria**:
  - Chatbot components respect the current theme context
  - Colors and styling match the active theme
  - Smooth transitions when theme changes
- **Test**: Verify chatbot appearance matches light/dark themes

### FR-5: Error Handling and Fallbacks
- **Requirement**: The chatbot must gracefully handle initialization errors
- **Acceptance Criteria**:
  - Shows fallback UI if chatbot fails to initialize
  - Logs initialization errors for debugging
  - Does not break the main application if chatbot fails
- **Test**: Verify graceful degradation when chatbot components fail

### FR-6: Responsiveness
- **Requirement**: The chatbot must behave appropriately on different screen sizes
- **Acceptance Criteria**:
  - Visible on desktop screens (≥768px width)
  - Hidden on mobile screens by default (configurable)
  - Responsive to window resize events
- **Test**: Verify behavior on different screen sizes

## User Scenarios

### Scenario 1: Authenticated User Experience
**Actor**: Authenticated user
**Trigger**: User navigates to any authenticated page
**Flow**:
1. User logs in successfully and receives JWT token
2. User navigates to dashboard or any authenticated page
3. Chatbot widget appears as floating button at bottom-right
4. User clicks chatbot button to expand chat panel
5. User can interact with AI assistant for todo tasks
**Success**: Chatbot is visible and functional for all authenticated pages

### Scenario 2: Unauthenticated User Experience
**Actor**: Unauthenticated user
**Trigger**: User visits login page or attempts access to authenticated areas
**Flow**:
1. User is not logged in
2. Chatbot widget remains hidden
3. User cannot access chatbot functionality
4. User must authenticate to see chatbot
**Success**: Chatbot is properly hidden from unauthenticated users

### Scenario 3: Theme Change Interaction
**Actor**: Authenticated user
**Trigger**: User toggles between light/dark theme
**Flow**:
1. User has chatbot open or closed
2. User changes theme preference
3. Chatbot UI updates to reflect new theme colors
4. Consistent appearance with rest of application
**Success**: Chatbot adapts to new theme without disruption

## Success Criteria

- **Quantitative Metrics**:
  - Chatbot appears on 100% of authenticated pages within 1 second of page load
  - 99% of authenticated sessions have visible chatbot UI
  - Zero impact on page load performance (>5% degradation threshold)
  - 100% of theme changes properly reflected in chatbot UI

- **Qualitative Measures**:
  - Users can discover and access chatbot functionality intuitively
  - Chatbot UI integrates seamlessly with existing application design
  - Authentication state properly controls chatbot visibility
  - Error conditions handled gracefully without impacting main app

## Key Entities

- **ChatWidget**: Floating button component that expands into chat panel
- **ChatAuthContext**: Authentication state management for chatbot
- **ChatKitWrapper**: Main chat interface component
- **ThemeContext**: Theme state that affects chatbot appearance
- **JWT Token**: Authentication token passed to chatbot API calls

## Constraints

- Backend logic and MCP tools remain unchanged
- Authentication system remains unchanged
- Chatbot functionality remains the same (only UI visibility fixed)
- No changes to existing UI components outside of chatbot integration
- Must maintain backward compatibility with existing application

## Assumptions

- Backend API endpoints for chatbot are functional
- MCP tools are properly configured
- JWT authentication system works as expected
- Existing chatbot components are functional once rendered
- Network connectivity is available for chatbot API calls

## Dependencies

- Authentication system (JWT-based)
- Theme context provider
- API client for chatbot communications
- Existing chatbot components and logic