# AI Chatbot Feature Documentation

## Overview
The AI Chatbot feature enables users to manage their tasks through natural language commands. It leverages an AI agent that understands natural language and maps user requests to specific task operations through MCP (Model Context Protocol) tools.

## Architecture

### Backend Components
1. **API Routes**: `/api/{user_id}/chat` endpoint in `backend/src/api/routes/chat.py`
2. **Services**:
   - `ChatService` (orchestrates the conversation flow)
   - `ConversationService` (manages conversation and message history)
3. **AI Agent**: `ChatAgent` using OpenAI SDK with Cohere models via compatibility API
4. **MCP Tools**: Direct function calls for task operations
5. **Data Models**: `Conversation` and `Message` SQLModels with relationships

### Frontend Components
1. **Chat Page**: Complete chat interface at `/chat`
2. **Components**: `ChatInterface`, `MessageList`, `ChatInput`
3. **API Client**: `chat-api.ts` for backend communication
4. **Storage**: `conversation-storage.ts` for maintaining conversation ID

## API Endpoints

### POST `/api/{user_id}/chat`

#### Request Body
```json
{
  "message": "Natural language command (required)",
  "conversation_id": 123 (optional, omit for new conversation)
}
```

#### Headers
- `Authorization: Bearer <jwt_token>`

#### Response
```json
{
  "conversation_id": 123,
  "response": "AI response message",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {...},
      "result": {...}
    }
  ]
}
```

## MCP Tools Available

### add_task
Creates a new task for the user.
- Parameters: `user_id`, `title` (required), `description` (optional)
- Returns: Task ID and creation status

### list_tasks
Lists user's tasks with optional status filter.
- Parameters: `user_id`, `status` ("all", "pending", "completed")
- Returns: List of tasks with metadata

### complete_task
Marks a task as completed.
- Parameters: `user_id`, `task_id`
- Returns: Completion status and task info

### update_task
Updates task title or description.
- Parameters: `user_id`, `task_id`, `title` (optional), `description` (optional)
- Returns: Update status and updated task info

### delete_task
Permanently deletes a task.
- Parameters: `user_id`, `task_id`
- Returns: Deletion status and task info

## Natural Language Examples

Users can interact with the chatbot using commands like:
- "Add a task to buy groceries"
- "Show me my tasks" / "What's on my todo list?"
- "Complete task 1" / "Mark the grocery task as done"
- "Update task 1 title to 'Buy food'"
- "Delete the grocery task"

## Security Features

- JWT authentication required on every request
- User ID validation ensures users can only access their own conversations and tasks
- Input sanitization for preventing injection attacks
- Rate limiting on API calls

## Error Handling

- Invalid JWT tokens return 401 Unauthorized
- User ID mismatches return 403 Forbidden
- Empty messages return 400 Bad Request
- Missing conversations return 404 Not Found
- AI service failures return 500 Internal Server Error

## Database Schema

### Conversations Table
- `id` (Primary Key)
- `user_id` (Foreign Key to users table)
- `created_at`
- `updated_at`

### Messages Table
- `id` (Primary Key)
- `conversation_id` (Foreign Key to conversations)
- `user_id` (Foreign Key to users)
- `role` ("user", "assistant", "system")
- `content`
- `tool_calls` (JSON string)
- `created_at`

## Testing

Run backend tests:
```bash
cd backend
pytest tests/test_chat_endpoint.py
pytest tests/test_ai_agent.py
pytest tests/test_mcp_tools.py
pytest tests/test_conversation_service.py
```

## Environment Variables

Required for backend:
```bash
COHERE_API_KEY=your_api_key
OPENAI_COMPAT_BASE_URL=https://api.cohere.ai/compatibility/v1
COHERE_MODEL_NAME=command-r-plus
```

## Troubleshooting

### Common Issues
1. **422 Validation Errors**: Usually caused by Cohere API parameter validation issues
2. **Authentication Failures**: Check JWT token validity and user_id parameter
3. **Tool Execution Failures**: Check that the user owns the tasks they're trying to modify

### Logging
- API calls are logged with user_id and conversation_id
- Tool executions are logged with execution time
- Error responses include descriptive error messages

## Performance Considerations

- Conversation history is loaded per request (stateless design)
- Database queries are optimized with proper indexes
- Target response time: < 5 seconds for simple commands
- Conversation history limits to prevent excessive load