# Quickstart Guide: AI-Powered Todo Chatbot Extension

**Feature**: AI-Powered Todo Chatbot Extension
**Date**: 2026-01-17

## Overview
This guide provides a quick setup for the AI-powered chatbot extension to the Todo application. The chatbot enables natural language interaction with the todo management system through OpenAI ChatKit and MCP tools.

## Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.9+ for backend services
- OpenAI API key
- MCP SDK access
- Running Todo application backend

## Environment Setup

### Frontend Configuration
1. Add required environment variables to `.env.local`:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   NEXT_PUBLIC_API_URL=http://localhost:8000/api
   NEXT_PUBLIC_MCP_ENDPOINT=http://localhost:8001
   ```

### Backend Configuration
1. Ensure the Todo application backend is running
2. Verify JWT authentication is working properly
3. Confirm existing task APIs are accessible

## Installation Steps

### 1. Install Frontend Dependencies
```bash
cd frontend
npm install @openai/chatkit-react @openai/agents
npm install @modelcontextprotocol/sdk
```

### 2. Install Backend Extensions
```bash
cd backend
pip install openai
pip install @modelcontextprotocol/sdk
```

### 3. Set Up MCP Tools
1. Create MCP tool definitions in `backend/src/mcp_tools/`
2. Implement authentication validation in each tool
3. Connect tools to existing service layer

### 4. Configure Chatbot Agent
1. Set up system prompt with domain knowledge
2. Configure intent recognition patterns
3. Connect to MCP tools

## Key Integration Points

### Frontend Integration
- Floating chatbot widget in `src/components/chatbot/widget.tsx`
- Theme compatibility in `src/components/chatbot/theme-provider.tsx`
- Session management in `src/hooks/use-chat-session.ts`

### Backend Integration
- MCP tools in `backend/src/mcp_tools/todo_operations.py`
- Authentication validation in `backend/src/mcp_tools/auth_middleware.py`
- Service layer connections in `backend/src/mcp_tools/service_adapters.py`

## Running the Application

### Development Mode
1. Start the backend:
   ```bash
   cd backend
   uvicorn src.main:app --reload
   ```

2. Start the MCP tools server:
   ```bash
   cd backend
   python -m src.mcp_tools.server
   ```

3. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

### Available Chat Commands
- "Add a task to buy groceries" - Creates a new task
- "Show my tasks" - Lists all pending tasks
- "Mark task 3 as complete" - Marks specific task as completed
- "Delete the assignment task" - Deletes a task
- "What tasks are completed?" - Shows completed tasks only

## Testing the Integration

### Manual Testing
1. Log in to the Todo application
2. Open the floating chatbot widget
3. Try various natural language commands
4. Verify tasks are created/updated/deleted properly
5. Confirm authentication is enforced

### API Testing
Use the following endpoints to test MCP tools directly:
- POST `/mcp/create_task` - Create a task
- POST `/mcp/list_tasks` - List tasks
- POST `/mcp/complete_task` - Complete a task
- POST `/mcp/delete_task` - Delete a task

## Troubleshooting

### Common Issues
1. **Authentication failures**: Verify JWT token is being passed correctly to MCP tools
2. **MCP connection errors**: Check that MCP server is running and accessible
3. **Rate limiting**: Ensure OpenAI API usage is within limits
4. **Theme inconsistencies**: Verify theme context is properly passed to chat components

### Debugging Tips
- Enable verbose logging in MCP tools
- Check browser console for client-side errors
- Monitor network requests for authentication issues
- Verify database operations are properly isolated by user

## Next Steps
1. Implement advanced natural language understanding
2. Add conversation history persistence
3. Implement more sophisticated intent recognition
4. Add comprehensive error handling and fallbacks