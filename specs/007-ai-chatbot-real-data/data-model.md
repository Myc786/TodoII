# Data Model: AI-Powered Todo Chatbot with Real Data Operations

## Overview
The chatbot will operate on the existing Task data model with proper user isolation through authentication.

## Existing Data Models Used

### Task Model
- **Source**: Backend task_service.py and database schema
- **Fields**:
  - `id`: string/UUID unique identifier for task
  - `title`: string task title
  - `description`: string optional task description
  - `completed`: boolean completion status
  - `user_id`: string foreign key linking to user who owns task
  - `created_at`: DateTime timestamp of creation
  - `updated_at`: DateTime timestamp of last update
  - `version`: number for optimistic locking

### User Model
- **Source**: Backend authentication system
- **Fields**:
  - `id`: string/UUID unique identifier for user
  - `email`: string user email for identification
  - `name`: string optional user name

### JWT Token Model
- **Source**: Authentication system
- **Fields**:
  - `user_id`: string user identifier from token payload
  - `exp`: number expiration timestamp
  - `iat`: number issued at timestamp

## MCP Tool Models

### MCP Tool Request
- **Source**: MCP tools framework
- **Fields**:
  - `tool_name`: string name of the tool to execute
  - `parameters`: object parameters for the tool
  - `user_id`: string authenticated user identifier

### MCP Tool Response
- **Source**: MCP tools framework
- **Fields**:
  - `success`: boolean whether the operation succeeded
  - `data`: object result data from the tool
  - `error`: string error message if operation failed

## Chat Message Models

### Chat Request
- **Source**: Frontend chat component
- **Fields**:
  - `message`: string user's natural language command
  - `user_id`: string authenticated user identifier (extracted from JWT)

### Chat Response
- **Source**: Backend chat endpoint
- **Fields**:
  - `message`: string natural language response to user
  - `success`: boolean whether the operation succeeded
  - `action`: string type of action taken
  - `task_id`: string optional task ID related to action

## Integration Points

### MCP Tool Integration
- The chatbot will route natural language commands to appropriate MCP tools
- MCP tools will operate on the Task model with user_id filtering
- JWT authentication will provide user_id for MCP tool calls

### Authentication Integration
- JWT tokens will be validated before MCP tool execution
- user_id from JWT will be used to filter Task operations
- All MCP tool calls will be scoped to the authenticated user

## Validation Rules

### Data Access Rules
- All Task operations must be filtered by user_id
- MCP tools must validate user_id before database operations
- Cross-user data access is prohibited

### Operation Validation
- Task titles must be between 1 and 200 characters
- Task operations must include valid user authentication
- MCP tool parameters must be properly validated

## Relationships

### Data Flow
```
User Input (natural language) -> LLM -> MCP Tool Selection -> MCP Tool Execution -> Database -> Result -> Natural Language Response
```

### Security Flow
```
JWT Token -> User ID Extraction -> MCP Tool Validation -> User-Isolated Database Operation -> Result
```

### Component Relationships
```
Frontend Chat Component -> API Client -> Backend Chat Endpoint -> MCP Tools -> Backend Services -> Database
```