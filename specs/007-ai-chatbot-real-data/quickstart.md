# Quickstart Guide: AI-Powered Todo Chatbot with Real Data Operations

## Overview
This guide provides instructions for implementing the AI-powered chatbot with MCP tool integration to operate on real application data.

## Prerequisites
- Node.js 18+ installed (for frontend)
- Python 3.9+ installed (for backend)
- PostgreSQL/Neon database with existing task data
- Existing authentication system with JWT tokens
- MCP tools framework installed and configured
- Running backend server with task API endpoints

## Installation Steps

### 1. Verify Existing Infrastructure
Ensure the following components are available:
- MCP tools framework with create_task, list_tasks, update_task, complete_task, delete_task tools
- Backend API with JWT authentication
- Database with existing task data
- Frontend with chatbot UI components

### 2. Update Backend Chat Endpoint
Modify `src/api/routes/chat.py` to integrate MCP tools:

```python
# The endpoint should validate JWT, extract user_id, and route to appropriate MCP tools
# based on the natural language command
```

### 3. Update Frontend API Client
Modify `frontend/src/lib/chatbot-api.ts` to call the enhanced backend endpoint:

```typescript
// Ensure the API client properly handles real data responses from MCP tools
// and manages authentication tokens
```

### 4. Configure MCP Tools
Ensure MCP tools are properly configured to:
- Accept user_id parameter for user isolation
- Call existing backend services
- Return structured responses for natural language conversion

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
- Open the chatbot widget
- Test natural language commands:
  - "Show my tasks" - Should return real tasks from database
  - "Add a task to submit report" - Should create real task in database
  - "Mark my last task as complete" - Should update real task in database
  - "Delete the grocery task" - Should delete real task from database

### 3. Test Security
- Verify that users can only access their own tasks
- Test authentication failure scenarios
- Confirm that MCP tools enforce user isolation

## Troubleshooting

### MCP Tool Execution Failures
- Verify MCP tools are properly configured
- Check that JWT validation is working correctly
- Confirm user_id is being passed to MCP tools

### Authentication Issues
- Ensure JWT tokens are properly included in requests
- Verify user_id extraction from JWT tokens
- Check that authentication middleware is functioning

### Data Isolation Problems
- Confirm all MCP tools filter by user_id
- Verify database queries are properly scoped
- Test that users cannot access other users' data