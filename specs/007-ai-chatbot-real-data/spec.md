# Specification: AI-Powered Todo Chatbot with Real Data Operations

## Problem Statement

The current AI-powered Todo Chatbot operates with simulated responses and does not interact with real application data. The chatbot must be enhanced to operate directly on authenticated user's Todo application data using MCP tools, eliminating mock, simulated, or hardcoded content.

## Core Requirement (Critical)

The AI chatbot MUST use:
- Real tasks stored in the Todo application database (Neon PostgreSQL)
- User-specific data only (filtered by user_id from JWT)
- Authenticated API access via MCP tools

The chatbot must NEVER:
- Generate fake task data
- Use placeholder responses
- Respond with simulated or demo-only text
- Bypass authentication or user isolation

## Objective

Create an AI-powered Todo Chatbot that:
- Operates on real application data from Neon PostgreSQL database
- Uses MCP tools for all data operations
- Maintains strict user isolation through JWT authentication
- Supports natural language commands for task management
- Provides accurate responses reflecting real-time database state

## Functional Requirements

### FR-1: Real Data Operations
- **Requirement**: Chatbot must read/write actual tasks from/to the database
- **Acceptance Criteria**:
  - All operations go through MCP tools (create_task, list_tasks, update_task, complete_task, delete_task)
  - No simulated or hardcoded responses allowed
  - Real-time database state reflected in chat responses
- **Test**: Verify that natural language commands create actual database changes

### FR-2: MCP Tool Integration
- **Requirement**: All chatbot actions must execute through MCP tools
- **Acceptance Criteria**:
  - LLM selects appropriate MCP tools based on user intent
  - MCP tools call existing backend logic
  - No direct database access from AI
  - No direct REST calls from AI
- **Test**: Trace chat commands through MCP tool execution

### FR-3: Authentication & User Isolation
- **Requirement**: Chatbot operates only for authenticated users with user-specific data access
- **Acceptance Criteria**:
  - JWT token required for every chatbot interaction
  - user_id extracted from JWT for all MCP tool calls
  - All operations filtered by user_id to prevent cross-user access
  - Authentication failures handled gracefully
- **Test**: Verify user A cannot access user B's tasks

### FR-4: Natural Language Processing
- **Requirement**: Support natural language commands for task management
- **Acceptance Criteria**:
  - "Show my tasks" → Executes list_tasks MCP tool
  - "Add a task to submit report" → Executes create_task MCP tool
  - "Mark my last task as complete" → Executes complete_task MCP tool
  - "Delete the grocery task" → Executes delete_task MCP tool
  - "Which tasks are completed?" → Executes list_tasks with completion filter
- **Test**: Verify each command type executes correct MCP tool

### FR-5: LLM Usage Constraints
- **Requirement**: LLM used only for intent understanding and tool selection
- **Acceptance Criteria**:
  - LLM performs intent understanding and tool selection
  - LLM generates natural language responses from tool results
  - LLM does not invent task data or bypass MCP tools
  - Clear separation between LLM and data operations
- **Test**: Verify LLM does not generate fake data

### FR-6: Frontend Chat Behavior
- **Requirement**: Chat UI displays real results and handles errors properly
- **Acceptance Criteria**:
  - Responses reflect actual database state changes
  - Authentication failures are surfaced clearly
  - MCP tool errors are displayed meaningfully
  - Loading states for MCP tool execution
- **Test**: Verify chat UI reflects database changes in real-time

## User Scenarios

### Scenario 1: Task Creation via Chat
**Actor**: Authenticated user
**Trigger**: User types "Add a task to submit monthly report"
**Flow**:
1. User authenticates and opens chat
2. User types natural language command
3. LLM identifies intent as task creation
4. LLM calls create_task MCP tool with extracted details
5. MCP tool creates task in database for user_id from JWT
6. Database insertion confirmed
7. LLM generates response from MCP tool result
**Success**: Task appears in user's task list and chat confirms creation

### Scenario 2: Task Completion via Chat
**Actor**: Authenticated user
**Trigger**: User types "Mark my meeting task as complete"
**Flow**:
1. User authenticated with valid JWT
2. LLM identifies intent as task completion
3. LLM calls list_tasks MCP tool to find matching task
4. LLM calls complete_task MCP tool with specific task_id
5. MCP tool updates task in database for user_id
6. Database update confirmed
7. LLM generates response from completion result
**Success**: Task marked as complete in both UI and database

### Scenario 3: Task Query via Chat
**Actor**: Authenticated user
**Trigger**: User types "Show me my completed tasks"
**Flow**:
1. User authenticated with valid JWT
2. LLM identifies intent as task query with completion filter
3. LLM calls list_tasks MCP tool with completion filter
4. MCP tool retrieves user-specific tasks from database
5. LLM generates natural language response from results
**Success**: User sees list of completed tasks from their account

### Scenario 4: Unauthenticated Access Attempt
**Actor**: Unauthenticated user
**Trigger**: User attempts to use chatbot without authentication
**Flow**:
1. User tries to interact with chatbot
2. JWT validation fails
3. Authentication error propagated to LLM
4. LLM generates appropriate error response
**Success**: User receives clear authentication error message

## Success Criteria

- **Quantitative Metrics**:
  - 100% of chat commands result in actual database operations
  - 99% of authenticated requests succeed with proper user isolation
  - <1% of commands bypass MCP tools or use simulated data
  - <5% latency increase compared to simulated responses

- **Qualitative Measures**:
  - Natural language commands reliably trigger correct MCP tools
  - User isolation maintained across all operations
  - Error handling provides clear feedback to users
  - Real-time database state reflected in chat responses

## Key Entities

- **ChatSession**: Represents ongoing conversation with LLM
- **MCPTool**: Available tools for data operations (create_task, list_tasks, etc.)
- **JWTToken**: Authentication token with user_id extraction
- **TaskRecord**: Database entity representing user tasks
- **UserIsolation**: Security mechanism ensuring user-specific data access

## Constraints

- Backend logic must remain unchanged (MCP tools call existing endpoints)
- Authentication system remains unchanged (JWT-based)
- Database schema remains unchanged (PostgreSQL/Neon)
- MCP tools must be used for all data operations
- No direct database access from AI components
- User isolation must be maintained at all times

## Assumptions

- MCP tools are properly configured and accessible
- JWT authentication system provides reliable user_id extraction
- Database connections are stable and performant
- LLM can reliably identify intents and select appropriate tools
- Existing backend endpoints support MCP tool integration

## Dependencies

- MCP tools framework for data operations
- JWT authentication system for user identification
- PostgreSQL/Neon database for task storage
- LLM service (Qwen/OpenAI) for intent processing
- Existing backend API endpoints for MCP tool calls