---
id: 1
title: Phase III AI Chatbot Specification
stage: spec
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: 1-ai-chatbot
branch: 001-ai-chatbot
user: system
command: /sp.specify
labels: ["spec", "ai-chatbot", "phase-iii", "mcp", "natural-language", "cohere"]
links:
  spec: specs/1-ai-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-ai-chatbot/spec.md
  - specs/1-ai-chatbot/checklists/requirements.md
tests:
  - Specification quality validation (all checks passed)
---

## Prompt

```text
/sp.specify
Phase III: Todo AI Chatbot – Natural Language Todo Management

Project Overview
Build a conversational AI chatbot for the existing Todo web app that allows users to manage tasks (CRUD) via natural language commands. The backend must remain stateless, persist conversation history in Neon PostgreSQL, and expose task operations via MCP tools. Use OpenAI Agents SDK for agent logic, but configure it to use Cohere models via Cohere's OpenAI Compatibility API (no native Cohere SDK for agents – route through OpenAI-compatible client).

Core Requirements
1. Stateless /api/{user_id}/chat endpoint (POST)
   - Input: { conversation_id?: number, message: string }
   - Output: { conversation_id: number, response: string, tool_calls?: array }
   - Always authenticate via JWT → extract user_id
   - Load/append conversation history from DB (conversations + messages tables)

2. Database Models (extend existing)
   - Conversation: id, user_id (fk), created_at, updated_at
   - Message: id, conversation_id, user_id, role ("user" | "assistant"), content, created_at
   - Use SQLModel + Alembic migrations

3. MCP Server (using Official MCP SDK)
   - Expose exactly these tools (MCP format):
     - add_task(user_id: str, title: str, description?: str) → {task_id, status: "created", title}
     - list_tasks(user_id: str, status?: "all"|"pending"|"completed") → array of tasks
     - complete_task(user_id: str, task_id: int) → {task_id, status: "completed", title}
     - delete_task(user_id: str, task_id: int) → {task_id, status: "deleted", title}
     - update_task(user_id: str, task_id: int, title?: str, description?: str) → {task_id, status: "updated", title}
   - All tools MUST enforce user_id ownership validation

4. AI Agent Logic
   - Use OpenAI Agents SDK (Python) → Agent + Runner
   - LLM: Cohere models (e.g. command-r-plus or command-a-03-2025) via Compatibility API
     - Client setup: OpenAI(base_url="https://api.cohere.ai/compatibility/v1", api_key=COHERE_API_KEY)
     - Model names: use Cohere-compatible names (check Cohere docs for latest)
   - Agent instructions: Understand natural language for CRUD, chain tools if needed, always confirm actions, handle errors gracefully
   - Provide friendly responses + action confirmations

5. Conversation Flow (per request – stateless)
   1. Authenticate & get user_id
   2. If no conversation_id → create new Conversation row
   3. Load all prior messages for this conversation + user_id
   4. Append new user message to DB
   5. Build message history array (for agent)
   6. Run OpenAI Agents SDK runner with MCP tools
   7. Store assistant response + tool results in messages table
   8. Return response to frontend

6. Integration with Existing Frontend
   - ChatKit UI (already built) → POST to /api/{user_id}/chat
   - Handle conversation_id persistence (localStorage / URL param)
   - Show loading, tool usage indicators if possible

Non-Functional
- Security: JWT on every chat request, strict user_id filtering in tools & queries
- Scalability: Fully stateless server (no in-memory sessions)
- Error handling: Graceful messages for "task not found", invalid input, etc.
- Logging: Trace agent steps, tool calls, DB ops (structured logging)
```

## Response snapshot

Created comprehensive Phase III specification for Todo AI Chatbot with natural language task management.

**Specification Structure**:

1. **User Scenarios** (6 prioritized stories):
   - P1: Create Task via Natural Language (core value)
   - P1: List and Query Tasks (equally critical)
   - P2: Complete and Update Tasks (important but UI fallback exists)
   - P2: Delete Tasks via Conversation (less frequent)
   - P3: Resume Conversations (UX enhancement)
   - P3: Handle Complex Multi-Step Commands (advanced capability)

2. **Requirements** (20 functional, 10 non-functional):
   - Stateless chat endpoint with JWT authentication
   - Full conversation history persistence in database
   - 5 MCP tools with user_id validation
   - OpenAI Agents SDK with Cohere via compatibility API
   - Natural language understanding and confirmations
   - Tool chaining support
   - Graceful error handling
   - Frontend conversation persistence
   - Complete user isolation

3. **Success Criteria** (12 measurable outcomes):
   - Task creation in < 10 seconds
   - List tasks in < 5 seconds
   - 90% command interpretation accuracy
   - < 1 second conversation history loading
   - Zero data leakage between users
   - Complete statelessness validation
   - 85% user satisfaction with confirmations
   - 90% error message clarity
   - Correct tool chaining in 80% of attempts

4. **Key Design Decisions**:
   - Cohere via OpenAI Compatibility (not direct SDK)
   - Full history reload per request (stateless)
   - Conversation + Message tables for persistence
   - MCP stdio transport for tool exposure
   - localStorage for conversation_id on frontend
   - JWT-extracted user_id (not URL parameter)

5. **Comprehensive Documentation**:
   - 8 edge cases with handling strategies
   - 12 assumptions documenting design choices
   - 8 dependencies on existing systems
   - 15 out-of-scope items defining boundaries
   - 4 related specifications for context

**Quality Validation**: All checklist items passed
- No implementation details in spec
- All requirements testable and unambiguous
- Success criteria measurable and technology-agnostic
- User scenarios independently testable
- Edge cases, dependencies, assumptions documented
- Scope clearly bounded

**Branch Created**: 001-ai-chatbot
**Files Created**:
- specs/1-ai-chatbot/spec.md (comprehensive specification)
- specs/1-ai-chatbot/checklists/requirements.md (quality validation)

## Outcome

- ✅ Impact: Complete Phase III specification ready for planning with 6 prioritized user stories, 30 requirements, 12 success criteria, and comprehensive documentation
- 🧪 Tests: Specification quality validation passed (16/16 checklist items)
- 📁 Files: 2 files created (spec.md, checklists/requirements.md)
- 🔁 Next prompts: Run `/sp.plan` to create architecture and implementation plan for AI chatbot feature
- 🧠 Reflection: Specification balances user value (natural language task management) with technical constraints (stateless design, MCP tools, Cohere via compatibility). Prioritized user stories enable incremental delivery. All requirements are testable and bounded by clear assumptions/dependencies.

## Evaluation notes (flywheel)

- Failure modes observed: None - specification complete without clarifications needed
- Graders run and results (PASS/FAIL): PASS - all quality criteria met
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase to design MCP tool architecture and stateless conversation flow implementation
