# Agent Context: AI-Powered Todo Chatbot Extension

**Feature**: AI-Powered Todo Chatbot Extension
**Date**: 2026-01-17

## Technology Stack Context

### OpenAI ChatKit Integration
- Use OpenAI ChatKit React components for chat interface
- Implement system prompt with domain-specific knowledge
- Utilize message history management for context
- Apply theme context to match existing application design

### MCP SDK Usage
- Implement MCP tools for all backend operations
- Ensure each tool validates JWT authentication
- Use existing service layer through MCP adapters
- Follow MCP protocol for structured tool calling

### Next.js 16+ App Router
- Integrate chatbot as client component in existing layout
- Use server actions where appropriate for MCP tool calls
- Maintain existing routing patterns and structure
- Leverage React Server Components for performance

## Implementation Guidelines

### Security Requirements
- Never access database directly from AI layer
- Validate JWT token in every MCP tool call
- Isolate user data using authenticated user context
- Sanitize all user inputs to prevent injection

### Performance Considerations
- Cache frequently accessed data where appropriate
- Optimize AI service calls to minimize latency
- Implement efficient message history management
- Use streaming responses where beneficial

### Integration Patterns
- Reuse existing backend service layer through MCP tools
- Maintain consistency with existing UI/UX patterns
- Follow established error handling patterns
- Preserve existing authentication flows

## Key Components to Implement

### Frontend Components
- FloatingChatWidget: Main entry point for chatbot
- ChatPanel: Expandable/collapsible chat interface
- MessageBubble: Styled messages for user/AI
- TypingIndicator: Visual feedback during AI processing
- ErrorMessage: User-friendly error displays

### MCP Tools
- create_task: Create new tasks from natural language
- list_tasks: Retrieve and format task lists
- complete_task: Update task completion status
- delete_task: Remove tasks safely
- update_task: Modify existing tasks

### Backend Services Integration
- Connect MCP tools to existing task service
- Maintain transaction integrity
- Preserve existing data validation
- Follow established error response patterns