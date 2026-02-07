# Implementation Plan: Todo AI Chatbot - Natural Language Todo Management

**Branch**: `001-ai-chatbot` | **Date**: 2026-02-06 | **Spec**: [specs/1-ai-chatbot/spec.md](../1-ai-chatbot/spec.md)
**Input**: Feature specification from `/specs/1-ai-chatbot/spec.md`

**Note**: This plan follows the Spec-Driven Development methodology. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Enable users to manage tasks through natural language conversations with an AI chatbot. The system uses a stateless chat endpoint that persists conversation history in PostgreSQL, exposes task operations via MCP tools, and uses OpenAI Agents SDK configured with Cohere models via OpenAI Compatibility API. Core value: faster task management with reduced friction through conversational interface.

**Primary Technical Approach**:
- Stateless FastAPI endpoint that loads full conversation history per request
- MCP server exposing 5 task operation tools with user_id validation
- OpenAI Agents SDK with Cohere LLM via compatibility API
- React ChatKit UI with localStorage for conversation persistence
- SQLModel database models for conversations and messages

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript/Next.js 14 (frontend)
**Primary Dependencies**:
- Backend: FastAPI, OpenAI SDK (for agents), MCP SDK, SQLModel, Alembic, Cohere (via OpenAI compatibility)
- Frontend: Next.js 14, React, OpenAI ChatKit UI library, existing auth context
**Storage**: Neon PostgreSQL (existing) + new tables (conversations, messages)
**Testing**: pytest (backend), Jest/React Testing Library (frontend), Playwright (E2E)
**Target Platform**: Web application (deployed on Vercel frontend + Hugging Face backend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**:
- Simple commands: < 5 seconds response time
- Complex commands: < 10 seconds response time
- Conversation history load: < 1 second for up to 100 messages
**Constraints**:
- Complete statelessness (no server-side sessions)
- JWT authentication on every request
- User_id filtering on all database queries and tool calls
- Cohere via OpenAI compatibility (not direct SDK)
**Scale/Scope**:
- Support conversations with 100+ messages
- Handle concurrent requests from same user
- Multi-user isolation with zero data leakage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Constitution Compliance

✅ **Simplicity**: Uses existing auth, database, and deployment infrastructure. Adds minimal new dependencies (OpenAI SDK, MCP SDK).

✅ **Security**: JWT authentication enforced on chat endpoint. All tool calls validate user_id ownership. No hardcoded secrets.

✅ **Code Quality**: Will follow existing FastAPI patterns, TypeScript standards, and test coverage requirements.

✅ **Performance**: Stateless design enables horizontal scaling. Database queries optimized with proper indexes.

⚠️ **Constraint**: Using Cohere via OpenAI compatibility adds indirection layer vs direct Cohere SDK. Justified because OpenAI Agents SDK doesn't support native Cohere client, and compatibility API provides standard interface.

**Gates Status**: PASS - No constitution violations. Constraint justified by technical requirements.

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-chatbot/
├── plan.md              # This file (architecture and implementation plan)
├── research.md          # Phase 0: MCP SDK, OpenAI Agents SDK, Cohere compatibility research
├── data-model.md        # Phase 1: Conversation/Message schema, MCP tool contracts
├── quickstart.md        # Phase 1: Local setup, testing, deployment guide
├── contracts/           # Phase 1: API endpoint specs, MCP tool definitions
│   ├── chat-endpoint.yaml
│   ├── mcp-tools.yaml
│   └── database-schema.sql
└── tasks.md             # Phase 2: Testable implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   └── routes/
│   │       └── chat.py              # NEW: /api/{user_id}/chat endpoint
│   ├── models/
│   │   ├── conversation.py          # NEW: Conversation SQLModel
│   │   ├── message.py               # NEW: Message SQLModel
│   │   └── task.py                  # EXISTING: Task model (used by MCP tools)
│   ├── services/
│   │   ├── chat_service.py          # NEW: Chat orchestration logic
│   │   ├── conversation_service.py  # NEW: Conversation history management
│   │   └── task_service.py          # EXISTING: Task CRUD (wrapped by MCP)
│   ├── mcp/
│   │   ├── __init__.py              # NEW: MCP server module
│   │   ├── server.py                # NEW: MCP server setup with stdio transport
│   │   ├── tools.py                 # NEW: 5 task operation tools
│   │   └── types.py                 # NEW: MCP tool input/output types
│   ├── ai/
│   │   ├── __init__.py              # NEW: AI agent module
│   │   ├── agent.py                 # NEW: OpenAI Agent setup with Cohere
│   │   ├── instructions.py          # NEW: Agent system prompt/instructions
│   │   └── config.py                # NEW: Cohere API config via OpenAI compatibility
│   └── main.py                      # MODIFIED: Register chat routes
├── migrations/
│   └── versions/
│       └── <timestamp>_add_conversations.py  # NEW: Alembic migration
└── tests/
    ├── test_chat_endpoint.py        # NEW: Chat API tests
    ├── test_mcp_tools.py            # NEW: MCP tool unit tests
    ├── test_conversation_service.py # NEW: History management tests
    └── test_ai_agent.py             # NEW: Agent integration tests

frontend/
├── src/
│   ├── app/
│   │   └── chat/
│   │       ├── page.tsx             # NEW: Chat page component
│   │       └── layout.tsx           # NEW: Chat layout (optional)
│   ├── components/
│   │   └── chat/
│   │       ├── chat-interface.tsx   # NEW: ChatKit integration
│   │       ├── message-list.tsx     # NEW: Message history display
│   │       ├── chat-input.tsx       # NEW: Message input with loading states
│   │       └── tool-indicator.tsx   # NEW: Visual indicator for tool execution
│   ├── lib/
│   │   ├── chat-api.ts              # NEW: Chat endpoint client functions
│   │   └── conversation-storage.ts  # NEW: localStorage conversation_id management
│   └── types/
│       └── chat.ts                  # NEW: Message, Conversation TypeScript types
└── tests/
    └── chat/
        ├── chat-interface.test.tsx  # NEW: Component tests
        └── e2e-chat.spec.ts         # NEW: End-to-end conversation tests
```

**Structure Decision**: Web application structure (backend + frontend). Backend adds new modules for chat, MCP, and AI agent logic. Frontend adds chat page with ChatKit UI components. All new code follows existing project conventions for routing, services, and testing.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations requiring complexity tracking. The Cohere compatibility layer constraint is documented above as acceptable indirection.*

## Phase 0: Research & Discovery

**Goal**: Verify technical feasibility and document integration patterns for MCP SDK, OpenAI Agents SDK, and Cohere compatibility API.

### Research Items

1. **MCP SDK Python Integration**
   - Official MCP SDK installation and setup
   - Stdio transport configuration for tool exposure
   - Tool registration patterns and type validation
   - Error handling and logging patterns
   - Documentation: How to create custom MCP servers

2. **OpenAI Agents SDK with Cohere**
   - OpenAI SDK installation (Python agents module)
   - Agent + Runner initialization patterns
   - Configuring custom base_url for Cohere compatibility
   - Model name format for Cohere (command-r-plus, command-a-03-2025)
   - Tool calling with MCP tools
   - Message history format and conversation state management
   - Documentation: OpenAI Agents SDK, Cohere OpenAI Compatibility docs

3. **Cohere OpenAI Compatibility API**
   - API endpoint: `https://api.cohere.ai/compatibility/v1`
   - Authentication: API key format
   - Supported models and naming conventions
   - Rate limits and error responses
   - Tool/function calling format compatibility
   - Documentation: Cohere compatibility API reference

4. **OpenAI ChatKit UI Library**
   - npm package name and version
   - React component exports (ChatInterface, MessageList, etc.)
   - Props and customization options
   - Styling and theming integration with existing design system
   - Message format requirements
   - Loading states and typing indicators
   - Documentation: ChatKit GitHub repo, examples

5. **Database Migration Strategy**
   - Alembic migration for conversations and messages tables
   - Foreign key constraints to existing users table
   - Index strategy for conversation history queries (user_id, conversation_id, created_at)
   - Migration rollback plan
   - Data retention and cleanup policies

### Research Outputs

- `specs/001-ai-chatbot/research.md`: Consolidated findings with code examples, API patterns, and integration decisions
- Proof-of-concept scripts (if needed): Simple MCP server, basic agent with Cohere, ChatKit example

### Success Criteria

- ✅ All 5 research items documented with working code examples
- ✅ No blocking technical issues identified
- ✅ Clear integration patterns established for MCP + OpenAI Agents + Cohere
- ✅ ChatKit UI library confirmed compatible with Next.js 14 App Router

## Phase 1: Architecture & Design

**Goal**: Define data models, API contracts, MCP tool specifications, and agent instructions. Create deployment and testing strategy.

### Design Deliverables

#### 1. Data Model Design (`data-model.md`)

**Conversation Model**:
```python
class Conversation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
```

**Message Model**:
```python
class Message(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    role: str = Field(...)  # "user" | "assistant" | "system"
    content: str = Field(...)
    tool_calls: str | None = Field(default=None)  # JSON string of tool calls
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
```

**Indexes**:
- `conversations`: (user_id), (user_id, created_at DESC)
- `messages`: (conversation_id, created_at ASC), (user_id)

**Design Decisions**:
- Tool calls stored as JSON string (not separate table) for simplicity
- Immutable messages (no updates after creation) for audit trail
- Updated_at on Conversation tracks last activity
- Foreign key cascades: DELETE conversation → DELETE messages

#### 2. API Contract Design (`contracts/chat-endpoint.yaml`)

**Endpoint**: `POST /api/{user_id}/chat`

**Request**:
```json
{
  "conversation_id": 123,  // optional, omit for new conversation
  "message": "Add a task to buy groceries"
}
```

**Response** (Success):
```json
{
  "conversation_id": 123,
  "response": "I've created a new task: 'Buy groceries'. Would you like to add a due date?",
  "tool_calls": [
    {
      "tool": "add_task",
      "arguments": {"user_id": "42", "title": "Buy groceries"},
      "result": {"task_id": 99, "status": "created", "title": "Buy groceries"}
    }
  ]
}
```

**Response** (Error):
```json
{
  "error": "AI service temporarily unavailable",
  "code": "AI_SERVICE_ERROR",
  "conversation_id": 123  // returned if conversation was loaded successfully
}
```

**Authentication**: JWT Bearer token in `Authorization` header. User_id extracted from token MUST match path parameter.

**Status Codes**:
- 200: Success
- 400: Invalid request (missing message, invalid conversation_id)
- 401: Unauthorized (missing/invalid JWT)
- 403: Forbidden (user_id mismatch or conversation ownership violation)
- 500: Server error (AI service failure, database error)

#### 3. MCP Tool Specifications (`contracts/mcp-tools.yaml`)

**Tool 1: add_task**
```yaml
name: add_task
description: Create a new task for the user
parameters:
  user_id:
    type: string
    required: true
    description: User ID from JWT authentication
  title:
    type: string
    required: true
    description: Task title extracted from user message
  description:
    type: string
    required: false
    description: Optional task description
returns:
  task_id: integer
  status: string  # "created"
  title: string
  description: string | null
```

**Tool 2: list_tasks**
```yaml
name: list_tasks
description: List user's tasks with optional status filter
parameters:
  user_id:
    type: string
    required: true
  status:
    type: string
    required: false
    enum: ["all", "pending", "completed"]
    default: "all"
returns:
  type: array
  items:
    task_id: integer
    title: string
    description: string | null
    status: string  # "pending" | "completed"
    created_at: string (ISO 8601)
```

**Tool 3: complete_task**
```yaml
name: complete_task
description: Mark a task as completed
parameters:
  user_id:
    type: string
    required: true
  task_id:
    type: integer
    required: true
returns:
  task_id: integer
  status: string  # "completed"
  title: string
errors:
  - NOT_FOUND: Task does not exist or not owned by user
```

**Tool 4: delete_task**
```yaml
name: delete_task
description: Permanently delete a task
parameters:
  user_id:
    type: string
    required: true
  task_id:
    type: integer
    required: true
returns:
  task_id: integer
  status: string  # "deleted"
  title: string
errors:
  - NOT_FOUND: Task does not exist or not owned by user
```

**Tool 5: update_task**
```yaml
name: update_task
description: Update task title or description
parameters:
  user_id:
    type: string
    required: true
  task_id:
    type: integer
    required: true
  title:
    type: string
    required: false
  description:
    type: string
    required: false
returns:
  task_id: integer
  status: string  # "updated"
  title: string
  description: string | null
errors:
  - NOT_FOUND: Task does not exist or not owned by user
  - VALIDATION: No fields provided for update
```

**Error Handling Pattern**:
All tools return errors in consistent format:
```json
{
  "error": "NOT_FOUND",
  "message": "Task #99 not found or access denied",
  "task_id": 99
}
```

#### 4. Agent Instructions Design (`ai/instructions.py`)

**System Prompt** (excerpt):
```
You are a helpful task management assistant. Users interact with you to manage their todo list via natural language.

You have access to these tools:
- add_task: Create new tasks
- list_tasks: Show user's tasks (all, pending, or completed)
- complete_task: Mark tasks as done
- update_task: Modify task title or description
- delete_task: Remove tasks permanently

Guidelines:
1. Always confirm actions with natural, friendly language
2. When users reference tasks by title, use list_tasks to find the task_id first
3. For ambiguous requests, ask clarifying questions
4. For errors (task not found, etc.), provide helpful suggestions
5. Support multi-step commands by chaining tools
6. Never reveal technical details (database IDs, API errors) to users

Examples:
User: "Add a task to buy groceries"
→ Call add_task with title="Buy groceries"
→ Respond: "I've created a new task: 'Buy groceries'. Anything else?"

User: "Show my tasks"
→ Call list_tasks with status="all"
→ Respond with formatted list: "Here are your tasks: 1. Buy groceries (pending)..."
```

#### 5. Quickstart Guide (`quickstart.md`)

Contents:
- Local development setup (dependencies, environment variables)
- Running MCP server in development mode
- Testing chat endpoint with curl/Postman examples
- Frontend development server setup
- Running automated tests (unit, integration, E2E)
- Deployment checklist (Vercel frontend, Hugging Face backend)
- Troubleshooting common issues

#### 6. Database Schema SQL (`contracts/database-schema.sql`)

```sql
-- Conversations table
CREATE TABLE conversation (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_conversation_user_id ON conversation(user_id);
CREATE INDEX idx_conversation_user_created ON conversation(user_id, created_at DESC);

-- Messages table
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    tool_calls TEXT,  -- JSON string
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_message_conversation ON message(conversation_id, created_at ASC);
CREATE INDEX idx_message_user_id ON message(user_id);
```

### Architecture Decision Records (ADRs)

**ADR Candidates** (to be created if user approves):

1. **ADR: Use Cohere via OpenAI Compatibility Instead of Direct Cohere SDK**
   - Context: Need agent framework with tool calling
   - Options: Direct Cohere SDK, LangChain, OpenAI Agents + Cohere compatibility
   - Decision: OpenAI Agents SDK + Cohere compatibility API
   - Rationale: OpenAI Agents SDK provides best-in-class agent runtime with tool calling, but doesn't support Cohere natively. Compatibility API provides standard OpenAI interface. Alternative would be LangChain (heavier, more complex) or direct Cohere SDK (no agent framework).
   - Trade-offs: Adds API indirection layer vs direct Cohere SDK, but gains mature agent runtime and standard interface.

2. **ADR: Stateless Server Design with Full History Reload Per Request**
   - Context: Need conversation context for AI agent, must support horizontal scaling
   - Options: In-memory sessions, Redis session cache, stateless with DB reload
   - Decision: Stateless with full conversation history loaded from PostgreSQL per request
   - Rationale: Simplifies deployment (no session store), enables horizontal scaling, survives server restarts, consistent with existing architecture. Database queries optimized with indexes.
   - Trade-offs: Higher database load vs session cache, but conversations typically < 100 messages (< 1 second query time).

3. **ADR: Store Tool Calls as JSON String vs Separate Table**
   - Context: Need to track which tools were executed for debugging/audit
   - Options: Separate tool_calls table with rows per call, JSON column in messages table
   - Decision: JSON string column in messages table
   - Rationale: Simpler schema, tool calls are always retrieved with parent message, no complex joins needed, sufficient for debugging/audit requirements.
   - Trade-offs: Cannot query individual tool calls easily, but this is not a current requirement.

### Phase 1 Success Criteria

- ✅ All data models defined with relationships and constraints
- ✅ API contract documented with request/response examples
- ✅ All 5 MCP tools specified with parameters, returns, and error cases
- ✅ Agent instructions written with examples and guidelines
- ✅ Database schema SQL ready for migration
- ✅ Quickstart guide complete with setup and testing instructions
- ✅ ADR candidates identified (pending user approval to create)

## Phase 2: Implementation Tasks

**Goal**: Break down implementation into testable, incremental tasks that can be executed independently. Create `tasks.md` using `/sp.tasks` command.

**Task Categories** (to be detailed in tasks.md):

1. **Database Layer**
   - Create Alembic migration for conversations and messages tables
   - Implement Conversation and Message SQLModel models
   - Add conversation_service for CRUD operations
   - Write unit tests for conversation history queries

2. **MCP Server**
   - Set up MCP server with stdio transport
   - Implement add_task tool with user_id validation
   - Implement list_tasks tool with status filtering
   - Implement complete_task tool with ownership check
   - Implement update_task tool
   - Implement delete_task tool
   - Write unit tests for each tool (success and error cases)
   - Integration test: MCP server end-to-end with all tools

3. **AI Agent**
   - Configure OpenAI client with Cohere base_url and API key
   - Create Agent with system instructions
   - Set up Runner with MCP tools integration
   - Implement message history formatter (convert DB messages to agent format)
   - Write integration test: agent processes commands and calls tools
   - Test error handling: AI service unavailable, invalid tool calls

4. **Chat API Endpoint**
   - Create /api/{user_id}/chat route with JWT authentication
   - Implement request validation (message, optional conversation_id)
   - Implement conversation loading/creation logic
   - Integrate agent runner with MCP tools
   - Store user message and assistant response in database
   - Return response with conversation_id and tool_calls
   - Write API tests: new conversation, resume conversation, auth errors, tool execution

5. **Frontend Chat UI**
   - Install and configure OpenAI ChatKit library
   - Create /chat page with ChatKit component
   - Implement conversation_id persistence in localStorage
   - Create chat API client functions (sendMessage, loadHistory)
   - Add loading indicators and typing states
   - Add tool execution indicators (visual feedback when agent calls tools)
   - Write component tests for message display, input, loading states
   - Write E2E test: full conversation flow with task creation

6. **Testing & Quality**
   - Unit tests: 80%+ coverage for new backend code
   - Integration tests: Chat endpoint, MCP tools, agent with tools
   - E2E tests: Full user workflows (P1 and P2 user stories)
   - Security tests: User_id filtering, JWT validation, ownership checks
   - Performance tests: Conversation history loading, response times
   - Error handling tests: AI service failure, invalid requests, task not found

7. **Documentation & Deployment**
   - Update README with chat feature setup instructions
   - Document environment variables (COHERE_API_KEY, etc.)
   - Create deployment guide for backend (Hugging Face) and frontend (Vercel)
   - Add monitoring/logging for chat endpoint and tool calls
   - Create runbook for common issues (AI service errors, slow responses)

### Dependencies Between Task Categories

```
Database Layer
    ↓
MCP Server (depends on database models for task operations)
    ↓
AI Agent (depends on MCP tools)
    ↓
Chat API Endpoint (depends on agent + database)
    ↓
Frontend Chat UI (depends on chat API)
    ↓
Testing & Quality (depends on all above)
    ↓
Documentation & Deployment (depends on all above)
```

### Task Execution Strategy

1. **Phase 2.1**: Database + MCP Server (parallel with database work)
2. **Phase 2.2**: AI Agent + Chat API Endpoint (sequential)
3. **Phase 2.3**: Frontend Chat UI
4. **Phase 2.4**: Testing & Quality (continuous throughout, comprehensive pass at end)
5. **Phase 2.5**: Documentation & Deployment

### Phase 2 Output

- `specs/001-ai-chatbot/tasks.md`: Detailed task breakdown with acceptance criteria, test cases, and dependencies
- Ready for `/sp.tasks` command to generate actionable task list

## Risk Analysis & Mitigation

### Top Risks

1. **Risk: Cohere OpenAI Compatibility API has limited functionality**
   - **Blast radius**: Cannot use OpenAI Agents SDK, need to rewrite with different framework
   - **Mitigation**: Phase 0 research validates tool calling and agent patterns work with Cohere compatibility. Proof-of-concept required before Phase 1.
   - **Contingency**: Fall back to LangChain with direct Cohere SDK (1-2 day rework)

2. **Risk: OpenAI ChatKit library not compatible with Next.js 14 App Router**
   - **Blast radius**: Need to build custom chat UI components (2-3 day delay)
   - **Mitigation**: Phase 0 research validates ChatKit works with App Router and React Server Components
   - **Contingency**: Use existing UI component library (shadcn/ui) to build custom chat interface

3. **Risk: Conversation history queries become slow with many messages**
   - **Blast radius**: Poor user experience (> 5 second response times)
   - **Mitigation**: Database indexes on (conversation_id, created_at). Phase 1 performance testing with 100-message conversations.
   - **Contingency**: Implement pagination (load last N messages), store conversation summary for context

### Monitoring & Guardrails

- **Response Time Monitoring**: Alert if p95 > 10 seconds for chat endpoint
- **Error Rate Monitoring**: Alert if error rate > 5% for AI service calls
- **Database Query Performance**: Log slow queries (> 1 second) for optimization
- **Rate Limiting**: Implement per-user rate limiting (e.g., 30 requests/minute) to prevent abuse

## Deployment Strategy

### Environment Variables

**Backend (.env)**:
```
COHERE_API_KEY=<cohere-api-key>
OPENAI_COMPAT_BASE_URL=https://api.cohere.ai/compatibility/v1
COHERE_MODEL_NAME=command-r-plus
DATABASE_URL=<neon-postgres-url>
JWT_SECRET=<existing-secret>
LOG_LEVEL=INFO
```

**Frontend (.env.local)**:
```
NEXT_PUBLIC_API_URL=<backend-url>
```

### Deployment Steps

1. **Backend (Hugging Face Spaces)**:
   - Run Alembic migration: `alembic upgrade head`
   - Deploy updated backend with new chat routes and MCP server
   - Verify health check endpoint
   - Test chat endpoint with curl

2. **Frontend (Vercel)**:
   - Deploy updated frontend with chat UI
   - Verify environment variables set correctly
   - Test chat page loads and connects to backend

3. **Post-Deployment Validation**:
   - E2E test: Create task via chat, verify in UI
   - E2E test: List tasks via chat, verify response
   - Monitor logs for errors or performance issues
   - Verify conversation persistence across page reloads

### Rollback Plan

- **Backend**: Revert to previous deployment (no database changes yet, migration is additive)
- **Frontend**: Revert to previous deployment (chat page is new, no impact on existing features)
- **Database**: If migration causes issues, rollback with `alembic downgrade -1`

## Non-Functional Requirements Validation

### Performance

- **Load testing**: Simulate 10 concurrent users with chat conversations
- **Database query optimization**: Analyze EXPLAIN plans for conversation history queries
- **Response time targets**: Monitor p50, p95, p99 latencies for chat endpoint

### Security

- **Authentication testing**: Verify JWT validation on every chat request
- **Authorization testing**: Verify user_id filtering prevents data leakage
- **Input validation**: Test SQL injection, XSS attempts in chat messages
- **Rate limiting**: Verify per-user rate limits prevent abuse

### Reliability

- **Error handling**: Test graceful degradation when AI service unavailable
- **Idempotency**: Verify duplicate messages don't create duplicate tasks
- **Data consistency**: Verify database transactions prevent partial writes
- **Logging**: Verify structured logs capture all agent steps and errors

### Observability

- **Metrics**: Chat endpoint request count, error rate, response time, tool call counts
- **Logs**: Structured logs with user_id, conversation_id, tool calls, execution time
- **Alerts**: Set up alerts for high error rate, slow responses, database connection issues

## Definition of Done

### Feature Complete Checklist

- [ ] All database migrations applied successfully
- [ ] All 5 MCP tools implemented and tested
- [ ] AI agent configured with Cohere and MCP tools
- [ ] Chat API endpoint returns correct responses
- [ ] Frontend chat UI displays messages and handles input
- [ ] Conversation persistence works across page reloads
- [ ] P1 user stories (create, list) validated in production
- [ ] P2 user stories (complete, update, delete) validated
- [ ] All unit tests passing (80%+ coverage)
- [ ] All integration tests passing
- [ ] E2E tests passing for core workflows
- [ ] Security tests passing (auth, user_id filtering)
- [ ] Performance tests passing (< 5s for simple commands)
- [ ] Documentation complete (README, quickstart, runbook)
- [ ] Deployment successful in production environments
- [ ] Monitoring and logging in place
- [ ] No critical or high severity bugs

### Acceptance Testing

**User Acceptance Test 1**: Create Task via Chat
1. User opens chat interface
2. User types "Add a task to buy groceries"
3. System creates task and responds with confirmation
4. User verifies task appears in task list UI
5. **PASS**: Task created with correct title, confirmation message is natural

**User Acceptance Test 2**: List Tasks via Chat
1. User has 3 existing tasks (2 pending, 1 completed)
2. User types "Show me my pending tasks"
3. System lists 2 pending tasks with task IDs and titles
4. **PASS**: Only pending tasks shown, response is formatted and readable

**User Acceptance Test 3**: Resume Conversation
1. User starts conversation, sends 2 messages
2. User closes browser and reopens chat
3. System loads previous 2 messages from history
4. User sends new message, system responds with context
5. **PASS**: Full history loaded, conversation continues seamlessly

### Success Metrics (Post-Launch)

- **Usage**: 50%+ of active users try chat feature within first week
- **Adoption**: 30%+ of tasks created via chat after 1 month
- **Performance**: p95 response time < 10 seconds
- **Reliability**: Error rate < 2% for chat endpoint
- **User Satisfaction**: 80%+ positive feedback on chat experience

## Next Steps

1. **Run `/sp.tasks`**: Generate detailed task breakdown in `tasks.md` with acceptance criteria
2. **Create ADRs** (if user approves): Document architectural decisions for Cohere compatibility, stateless design, JSON tool calls
3. **Phase 0 Research**: Validate MCP SDK, OpenAI Agents SDK, Cohere compatibility API, ChatKit UI library
4. **Phase 1 Design**: Create data-model.md, contracts/, quickstart.md with detailed specifications
5. **Phase 2 Implementation**: Execute tasks from tasks.md in order, with continuous testing

---

**Plan Status**: DRAFT - Pending user review and Phase 0 research validation

**Questions for User**:
1. Should we create the 3 ADRs identified in this plan to document key architectural decisions?
2. Are there any additional performance or security requirements beyond what's specified?
3. Should we implement conversation pagination/limits initially, or defer until performance testing shows it's needed?
4. Do you want P3 user stories (resume conversations, multi-step commands) in MVP, or should we defer to future iteration?
