# Tasks: Todo AI Chatbot - Natural Language Todo Management

**Input**: Design documents from `/specs/001-ai-chatbot/`
**Prerequisites**: plan.md, spec.md, research.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- **Migrations**: `backend/migrations/versions/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Install dependencies and configure environment for AI chatbot feature

- [X] T001 Add OpenAI SDK dependency to backend/requirements.txt (openai>=1.0.0)
- [X] T002 [P] Add MCP SDK dependency to backend/requirements.txt (mcp)
- [X] T003 [P] Add environment variables to backend/.env: COHERE_API_KEY, OPENAI_COMPAT_BASE_URL, COHERE_MODEL_NAME
- [X] T004 [P] Install chat UI library in frontend: npm install react-chatbot-kit @chatscope/chat-ui-kit-react (if OpenAI ChatKit unavailable)
- [X] T005 Create backend/src/mcp/ module structure (__init__.py, server.py, tools.py, types.py)
- [X] T006 [P] Create backend/src/ai/ module structure (__init__.py, agent.py, instructions.py, config.py)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Database models and MCP server infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Database Layer

- [X] T007 Create Alembic migration for conversation table in backend/migrations/versions/<timestamp>_add_conversations.py
- [X] T008 Create Alembic migration for message table in backend/migrations/versions/<timestamp>_add_messages.py
- [X] T009 Create Conversation SQLModel in backend/src/models/conversation.py with relationships
- [X] T010 [P] Create Message SQLModel in backend/src/models/message.py with relationships
- [X] T011 Create ConversationService in backend/src/services/conversation_service.py (CRUD operations, history loading)
- [X] T012 Run migrations: alembic upgrade head to create conversation and message tables

### MCP Server Foundation

- [X] T013 Implement MCP tool type definitions in backend/src/mcp/types.py (TaskToolInput, TaskToolOutput)
- [X] T014 Implement add_task MCP tool in backend/src/mcp/tools.py with user_id validation
- [X] T015 [P] Implement list_tasks MCP tool in backend/src/mcp/tools.py with status filtering
- [X] T016 [P] Implement complete_task MCP tool in backend/src/mcp/tools.py with ownership check
- [X] T017 [P] Implement update_task MCP tool in backend/src/mcp/tools.py
- [X] T018 [P] Implement delete_task MCP tool in backend/src/mcp/tools.py
- [ ] T019 Configure MCP server setup in backend/src/mcp/server.py with SSE transport for FastAPI
- [ ] T020 Register all 5 MCP tools with server in backend/src/mcp/server.py

### AI Agent Foundation

- [X] T021 Configure OpenAI client with Cohere base_url in backend/src/ai/config.py
- [X] T022 Create agent system instructions in backend/src/ai/instructions.py (natural language guidelines, tool usage examples)
- [X] T023 Implement Agent initialization in backend/src/ai/agent.py using OpenAI SDK with Cohere config
- [X] T024 Implement message history formatter in backend/src/ai/agent.py (convert DB messages to agent format)
- [X] T025 Implement agent runner with MCP tools integration in backend/src/ai/agent.py

**Checkpoint**: Foundation ready - MCP tools registered, agent configured, database models created

---

## Phase 3: User Story 1 - Create Task via Natural Language (Priority: P1) 🎯 MVP

**Goal**: Users can create tasks by typing natural language commands like "Add a task to buy groceries"

**Independent Test**: Send chat message "Add a task to buy groceries", verify task created in database with correct title and confirmation response

### Backend Implementation for User Story 1

- [X] T026 [US1] Create ChatRequest schema in backend/src/models/chat_schemas.py (conversation_id, message)
- [X] T027 [P] [US1] Create ChatResponse schema in backend/src/models/chat_schemas.py (conversation_id, response, tool_calls)
- [X] T028 [US1] Create ChatService in backend/src/services/chat_service.py with process_message method
- [X] T029 [US1] Implement conversation loading/creation logic in ChatService (load history or create new conversation)
- [X] T030 [US1] Implement agent execution in ChatService (call agent with message history and MCP tools)
- [X] T031 [US1] Implement message persistence in ChatService (save user message and assistant response)
- [X] T032 [US1] Create POST /api/{user_id}/chat endpoint in backend/src/api/routes/chat.py with JWT authentication
- [X] T033 [US1] Implement request validation in chat endpoint (check message presence, validate conversation_id)
- [X] T034 [US1] Integrate ChatService with chat endpoint (call service, return response)
- [X] T035 [US1] Add error handling for AI service failures in chat endpoint (return 500 with user-friendly message)
- [X] T036 [US1] Register chat routes in backend/src/main.py

### Frontend Implementation for User Story 1

- [X] T037 [P] [US1] Create Message and Conversation TypeScript types in frontend/src/types/chat.ts
- [X] T038 [P] [US1] Create conversation storage utility in frontend/src/lib/conversation-storage.ts (localStorage get/set)
- [X] T039 [US1] Create chat API client functions in frontend/src/lib/chat-api.ts (sendMessage, loadHistory)
- [X] T040 [US1] Create chat page component in frontend/src/app/chat/page.tsx
- [X] T041 [US1] Create ChatInput component in frontend/src/components/chat/chat-input.tsx with loading state
- [X] T042 [P] [US1] Create MessageList component in frontend/src/components/chat/message-list.tsx
- [X] T043 [US1] Create ChatInterface component in frontend/src/components/chat/chat-interface.tsx (integrates MessageList and ChatInput)
- [X] T044 [US1] Implement conversation_id persistence in ChatInterface (load from localStorage, save on response)
- [X] T045 [US1] Implement message sending in ChatInterface (call API, update local state, handle errors)
- [X] T046 [US1] Add loading indicators to ChatInput (disable input, show spinner during API call)
- [X] T047 [US1] Add authentication check in chat page (redirect to login if not authenticated)

**Checkpoint**: User Story 1 complete - Users can create tasks via chat, see confirmation, task persisted in database

---

## Phase 4: User Story 2 - List and Query Tasks (Priority: P1)

**Goal**: Users can view their tasks by typing "Show me my pending tasks" or "What's on my todo list?"

**Independent Test**: Create 3 test tasks, send chat message "List my pending tasks", verify response lists all 3 tasks with IDs and titles

### Backend Implementation for User Story 2

- [X] T048 [US2] Update agent instructions in backend/src/ai/instructions.py with task listing examples and formatting guidelines
- [ ] T049 [US2] Test list_tasks MCP tool with different status filters (all, pending, completed) in backend/tests/test_mcp_tools.py
- [ ] T050 [US2] Verify agent correctly calls list_tasks tool for queries like "show my tasks" in backend/tests/test_ai_agent.py

### Frontend Implementation for User Story 2

- [X] T051 [US2] Update MessageList component to format task lists nicely (numbered, status indicators) in frontend/src/components/chat/message-list.tsx
- [X] T052 [US2] Add styling for task list display in chat messages (pending/completed badges) in frontend/src/components/chat/message-list.tsx

**Checkpoint**: User Stories 1 AND 2 complete - Users can create and list tasks via chat

---

## Phase 5: User Story 3 - Complete and Update Tasks (Priority: P2)

**Goal**: Users can complete or update tasks by typing "Complete task 5" or "Update task 3 title to 'Call John at 3pm'"

**Independent Test**: Create task, send "Complete task [id]", verify task marked complete in database and confirmation received

### Backend Implementation for User Story 3

- [ ] T053 [US3] Update agent instructions with task completion and update examples in backend/src/ai/instructions.py
- [ ] T054 [US3] Update agent instructions with tool chaining pattern (list_tasks then complete_task for title-based completion) in backend/src/ai/instructions.py
- [ ] T055 [US3] Test complete_task MCP tool with valid and invalid task IDs in backend/tests/test_mcp_tools.py
- [ ] T056 [P] [US3] Test update_task MCP tool with title and description updates in backend/tests/test_mcp_tools.py
- [ ] T057 [US3] Test agent correctly chains tools for "Mark buy groceries as done" (list then complete) in backend/tests/test_ai_agent.py

### Frontend Implementation for User Story 3

- [ ] T058 [US3] Add visual feedback for task completion confirmations in MessageList in frontend/src/components/chat/message-list.tsx
- [ ] T059 [US3] Add visual feedback for task update confirmations in MessageList in frontend/src/components/chat/message-list.tsx

**Checkpoint**: User Stories 1, 2, AND 3 complete - Full CRUD via chat (create, list, complete, update)

---

## Phase 6: User Story 4 - Delete Tasks via Conversation (Priority: P2)

**Goal**: Users can delete tasks by typing "Delete task 7" or "Remove the task about buying groceries"

**Independent Test**: Create task, send "Delete task [id]", verify task removed from database and confirmation received

### Backend Implementation for User Story 4

- [ ] T060 [US4] Update agent instructions with task deletion examples and confirmation patterns in backend/src/ai/instructions.py
- [ ] T061 [US4] Test delete_task MCP tool with valid and invalid task IDs in backend/tests/test_mcp_tools.py
- [ ] T062 [US4] Test agent handles "delete task" ambiguous requests by asking for clarification in backend/tests/test_ai_agent.py
- [ ] T063 [US4] Test agent chains tools for title-based deletion (list then delete) in backend/tests/test_ai_agent.py

### Frontend Implementation for User Story 4

- [ ] T064 [US4] Add visual feedback for deletion confirmations in MessageList (destructive action styling) in frontend/src/components/chat/message-list.tsx

**Checkpoint**: User Stories 1-4 complete - Full CRUD including deletion via chat

---

## Phase 7: User Story 5 - Resume Conversations (Priority: P3)

**Goal**: Users can close browser and return later, conversation history loads automatically

**Independent Test**: Start conversation with 5 messages, close browser, reopen chat page, verify all 5 messages displayed

### Backend Implementation for User Story 5

- [ ] T065 [US5] Add GET /api/{user_id}/conversations endpoint in backend/src/api/routes/chat.py to list user's conversations
- [ ] T066 [US5] Add GET /api/{user_id}/conversations/{conversation_id}/messages endpoint to fetch conversation history
- [ ] T067 [US5] Test conversation history loading for conversations with 50+ messages (performance check) in backend/tests/test_conversation_service.py

### Frontend Implementation for User Story 5

- [ ] T068 [US5] Implement conversation history loading on chat page mount in frontend/src/app/chat/page.tsx
- [ ] T069 [US5] Add conversation selector UI (dropdown or sidebar) to switch between past conversations in frontend/src/components/chat/chat-interface.tsx
- [ ] T070 [US5] Implement "New Conversation" button to start fresh conversation in frontend/src/components/chat/chat-interface.tsx
- [ ] T071 [US5] Add auto-scroll to latest message when conversation loads in frontend/src/components/chat/message-list.tsx

**Checkpoint**: User Story 5 complete - Conversation persistence and resumption working

---

## Phase 8: User Story 6 - Handle Complex Multi-Step Commands (Priority: P3)

**Goal**: Users can execute multiple operations in one request like "Show my tasks, complete the one about groceries, and add a new task"

**Independent Test**: Send multi-part command, verify each operation executes and cumulative confirmation returned

### Backend Implementation for User Story 6

- [ ] T072 [US6] Update agent instructions with multi-step command examples and execution order in backend/src/ai/instructions.py
- [ ] T073 [US6] Update agent instructions with partial failure handling (report successes and failures) in backend/src/ai/instructions.py
- [ ] T074 [US6] Test agent executes multi-step commands correctly in backend/tests/test_ai_agent.py
- [ ] T075 [US6] Test agent handles partial failures gracefully (one operation fails, others succeed) in backend/tests/test_ai_agent.py

### Frontend Implementation for User Story 6

- [ ] T076 [US6] Add visual formatting for multi-step confirmations (grouped operations, success/failure icons) in frontend/src/components/chat/message-list.tsx

**Checkpoint**: All user stories complete - Full chatbot functionality with advanced multi-step support

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Error handling, security, performance, and documentation improvements

### Error Handling & Security

- [ ] T077 [P] Add rate limiting to chat endpoint (30 requests/minute per user) in backend/src/api/routes/chat.py
- [ ] T078 [P] Add input validation for message length (max 1000 chars) in backend/src/api/routes/chat.py
- [ ] T079 [P] Test JWT validation on chat endpoint (reject invalid tokens) in backend/tests/test_chat_endpoint.py
- [ ] T080 [P] Test user_id filtering prevents data leakage (user A cannot access user B's tasks) in backend/tests/test_mcp_tools.py
- [ ] T081 Add comprehensive error handling for Cohere API failures in backend/src/ai/agent.py
- [ ] T082 [P] Add retry logic for transient Cohere API errors in backend/src/ai/agent.py

### Performance & Monitoring

- [ ] T083 [P] Add structured logging for all tool calls with execution time in backend/src/mcp/tools.py
- [ ] T084 [P] Add structured logging for agent invocations with conversation_id and user_id in backend/src/ai/agent.py
- [ ] T085 Verify conversation history loading performance (< 1 second for 100 messages) in backend/tests/test_conversation_service.py
- [ ] T086 [P] Add database indexes for conversation queries (user_id, created_at) via Alembic migration
- [ ] T087 [P] Add database indexes for message queries (conversation_id, created_at) via Alembic migration

### Frontend Polish

- [ ] T088 [P] Add ToolIndicator component to show when agent is calling tools in frontend/src/components/chat/tool-indicator.tsx
- [ ] T089 [P] Add typing indicator animation while waiting for AI response in frontend/src/components/chat/chat-input.tsx
- [ ] T090 Add mobile responsive styling for chat interface in frontend/src/components/chat/chat-interface.tsx
- [ ] T091 [P] Add error toast notifications for API failures in frontend/src/app/chat/page.tsx
- [ ] T092 Add "Retry" button for failed messages in frontend/src/components/chat/message-list.tsx

### Documentation

- [ ] T093 [P] Create quickstart guide in specs/001-ai-chatbot/quickstart.md (local setup, environment variables, testing)
- [ ] T094 [P] Update main README.md with chat feature section and setup instructions
- [ ] T095 Document MCP tool API contracts in specs/001-ai-chatbot/contracts/mcp-tools.yaml
- [ ] T096 [P] Document chat endpoint API in specs/001-ai-chatbot/contracts/chat-endpoint.yaml
- [ ] T097 Create deployment guide for Vercel (frontend) and Hugging Face (backend) in specs/001-ai-chatbot/DEPLOYMENT.md
- [ ] T098 [P] Create troubleshooting runbook for common issues (AI service errors, slow responses) in specs/001-ai-chatbot/TROUBLESHOOTING.md

### Testing

- [ ] T099 Write E2E test for User Story 1 (create task via chat) in frontend/tests/chat/e2e-chat.spec.ts
- [ ] T100 [P] Write E2E test for User Story 2 (list tasks via chat) in frontend/tests/chat/e2e-chat.spec.ts
- [ ] T101 [P] Write E2E test for User Story 3 (complete task via chat) in frontend/tests/chat/e2e-chat.spec.ts
- [ ] T102 Write integration test for chat endpoint with new conversation in backend/tests/test_chat_endpoint.py
- [ ] T103 [P] Write integration test for chat endpoint with existing conversation in backend/tests/test_chat_endpoint.py
- [ ] T104 [P] Write unit tests for ConversationService in backend/tests/test_conversation_service.py
- [ ] T105 Verify test coverage >= 80% for new backend code in backend/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-8)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if multiple developers)
  - Or sequentially in priority order (P1 → P1 → P2 → P2 → P3 → P3)
- **Polish (Phase 9)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Depends on Foundational (Phase 2) - Independent of US1 but builds on same infrastructure
- **User Story 3 (P2)**: Depends on Foundational (Phase 2) - May use list_tasks from US2 for tool chaining
- **User Story 4 (P2)**: Depends on Foundational (Phase 2) - Independent but similar to US3
- **User Story 5 (P3)**: Depends on Foundational (Phase 2) - Enhances conversation UX
- **User Story 6 (P3)**: Depends on Foundational (Phase 2) - Requires all MCP tools working (US1-4)

### Within Each User Story

- Backend implementation before frontend (API must exist before UI can call it)
- Models before services before endpoints
- Core implementation before polish
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 Setup**: Tasks T001-T006 all [P] can run in parallel
- **Phase 2 Foundational**:
  - Database migrations (T007-T008) can run in parallel
  - Database models (T009-T010) can run in parallel
  - MCP tools (T015-T018) can run in parallel after T014
  - AI agent components (T021-T022) can run in parallel
- **Within User Stories**:
  - Backend and frontend type definitions can run in parallel
  - Multiple MCP tool tests can run in parallel
  - Documentation tasks can run in parallel
  - E2E tests for different stories can run in parallel

---

## Parallel Example: Foundational Phase (Phase 2)

```bash
# Launch database setup in parallel:
Task T007: "Create Alembic migration for conversation table"
Task T008: "Create Alembic migration for message table"

# Launch model creation in parallel:
Task T009: "Create Conversation SQLModel"
Task T010: "Create Message SQLModel"

# Launch MCP tool implementation in parallel (after T014):
Task T015: "Implement list_tasks MCP tool"
Task T016: "Implement complete_task MCP tool"
Task T017: "Implement update_task MCP tool"
Task T018: "Implement delete_task MCP tool"

# Launch AI config in parallel:
Task T021: "Configure OpenAI client with Cohere"
Task T022: "Create agent system instructions"
```

---

## Parallel Example: User Story 1 (Phase 3)

```bash
# Launch type definitions in parallel:
Task T026: "Create ChatRequest schema"
Task T027: "Create ChatResponse schema"

# Launch frontend types and utilities in parallel:
Task T037: "Create TypeScript types for chat"
Task T038: "Create conversation storage utility"

# Launch frontend components in parallel (after T040):
Task T041: "Create ChatInput component"
Task T042: "Create MessageList component"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T025) - CRITICAL
3. Complete Phase 3: User Story 1 (T026-T047) - Create tasks
4. Complete Phase 4: User Story 2 (T048-T052) - List tasks
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Deploy minimal viable chatbot (create + list)

### Incremental Delivery

1. **Foundation** (Phases 1-2) → Database, MCP, Agent ready
2. **MVP Release** (Phases 3-4) → Create + List tasks via chat
3. **Enhanced Release** (Phases 5-6) → Add Complete, Update, Delete
4. **Advanced Release** (Phases 7-8) → Resume conversations, Multi-step commands
5. **Production Release** (Phase 9) → Polish, security, monitoring, documentation

### Parallel Team Strategy

With multiple developers:

1. **Team completes Setup + Foundational together** (Phases 1-2)
2. **Once Foundational is done**, split work:
   - Developer A: User Story 1 (Phase 3) - Create tasks
   - Developer B: User Story 2 (Phase 4) - List tasks
   - Developer C: Start Polish tasks (Phase 9) - Documentation, testing infrastructure
3. **After US1 + US2 complete**, continue:
   - Developer A: User Story 3 (Phase 5) - Complete/Update
   - Developer B: User Story 4 (Phase 6) - Delete
   - Developer C: Continue Polish
4. **P3 stories (optional)**:
   - Developer A or B: User Stories 5-6 (Phases 7-8)
   - All: Final polish and E2E testing

---

## Total Task Count

- **Phase 1 (Setup)**: 6 tasks
- **Phase 2 (Foundational)**: 19 tasks (BLOCKING)
- **Phase 3 (US1 - Create)**: 22 tasks (MVP critical)
- **Phase 4 (US2 - List)**: 5 tasks (MVP critical)
- **Phase 5 (US3 - Complete/Update)**: 7 tasks
- **Phase 6 (US4 - Delete)**: 5 tasks
- **Phase 7 (US5 - Resume)**: 7 tasks
- **Phase 8 (US6 - Multi-step)**: 5 tasks
- **Phase 9 (Polish)**: 29 tasks

**Total**: 105 tasks

**MVP Scope** (Phases 1-4): 52 tasks
**Full Feature** (All phases): 105 tasks

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label (US1, US2, etc.) maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group of related tasks
- Stop at any checkpoint to validate story independently
- **Avoid**: vague tasks, same file conflicts, cross-story dependencies that break independence
- **MCP tools must validate user_id ownership** on every operation (security critical)
- **All chat requests must authenticate via JWT** (security critical)
- **Stateless design**: Every request reloads conversation history from database
