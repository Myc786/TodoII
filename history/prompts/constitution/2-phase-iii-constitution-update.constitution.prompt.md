---
id: 2
title: Phase III Constitution Update
stage: constitution
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: ai-chatbot
branch: 1-fix-task-network-error
user: system
command: /sp.constitution
labels: ["constitution", "phase-iii", "ai-chatbot", "mcp", "stateless-architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Manual validation of constitution completeness
---

## Prompt

```text
/sp.constitution
Project: Todo AI Chatbot - Phase III (Natural Language Todo Management)
Core principles:
- Strictly follow spec-driven Agentic Dev Stack: spec → plan → tasks → implement (no manual coding)
- Use MCP (Model Context Protocol) as the core interface for AI ↔ Todo operations
- Stateless backend architecture: NO server-side session memory — all conversation state in Neon DB
- 100% user isolation: every tool / DB operation MUST filter by authenticated user_id (from JWT)
- Security first: JWT validation on every /api/chat request, tool calls MUST include & verify user_id
- Evaluation focus: clean prompts, spec quality, iteration traceability, final demo reliability

Fixed technology stack (do NOT suggest alternatives without explicit constitution update):
- Frontend: OpenAI ChatKit (React/Next.js compatible component for chat UI)
- Backend: Python FastAPI
- AI logic: OpenAI Agents SDK (agent + runner)
- Tool exposure: Official MCP SDK (build MCP server exposing Todo tools)
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
  - Tables: tasks (existing), conversations (user_id, id, created_at, updated_at), messages (user_id, conversation_id, role, content, created_at)
- Authentication: Better Auth → JWT tokens (shared secret via env var BETTER_AUTH_SECRET)
- Chat endpoint: POST /api/chat (stateless, uses conversation_id or creates new)

Key non-negotiable rules:
- All MCP tools MUST:
  - Require user_id (string) as first/mandatory parameter
  - Validate ownership (task.user_id == provided user_id)
  - Return consistent format: {"task_id": int, "status": str, "title": str} or array for list
  - Tools list: add_task, list_tasks, complete_task, delete_task, update_task (exact names & behaviors as in spec)
- Agent behavior:
  - Use OpenAI Agents SDK runner
  - Chain tools when needed (e.g. list → delete)
  - Always confirm actions in natural language ("Task 'Buy groceries' added successfully!")
  - Handle errors gracefully ("I couldn't find task #99 – maybe check the list?")
- Conversation flow (stateless):
  1. Load history from DB (messages JOIN conversations WHERE conversation_id = ? AND user_id = ?)
  2. Append new user message → store it
  3. Run agent with full message history + MCP tools
  4. Store assistant response + any tool results
  5. Return {conversation_id, response, tool_calls?}
- Frontend (ChatKit):
  - Use domain allowlist config for production (NEXT_PUBLIC_OPENAI_DOMAIN_KEY)
  - Handle streaming if supported, show loading/thinking states
  - Persist conversation_id in localStorage or URL for resume

Code quality standards:
- Python: type hints everywhere, Pydantic v2, black + ruff, HTTPException for errors
- FastAPI: APIRouter, Depends for auth & DB session
- MCP server: use official MCP SDK transports (stdio / http / sse preferred)
- No shared state in FastAPI – always reload from DB
- Logging: structured logs for agent steps, tool calls, errors

Deliverable checklist:
- Working stateless /api/chat endpoint
- MCP server exposing 5 Todo tools
- Conversations + messages tables in Neon DB
- OpenAI Agents SDK integration
- ChatKit UI integrated
- JWT authentication on every chat request
- All tools validate user_id and ownership
- Natural language confirmations
- Graceful error handling
- Conversation history persistence
```

## Response snapshot

Updated constitution to version 2.0.0 with comprehensive Phase III requirements:

**Major Changes**:
1. **Added 3 new principles**:
   - Stateless Architecture (Phase III requirement)
   - MCP Tool Design (Phase III critical)
   - AI Agent Behavior (Phase III)

2. **Enhanced existing principles**:
   - Security First Architecture → expanded with MCP user_id validation rules
   - Tech Stack Adherence → added Phase III stack (OpenAI Agents SDK, MCP, ChatKit)

3. **Added new sections**:
   - Conversation Flow (stateless implementation protocol)
   - Code Quality Standards (Python/TypeScript/MCP specific)
   - Testing & Validation (tool ownership, stateless behavior tests)
   - Deliverable Checklist (Phase III completion criteria)

4. **Database schema updates**:
   - Added `conversations` table
   - Added `messages` table with tool_calls JSON field

5. **Environment variables**:
   - Added `OPENAI_API_KEY` (backend)
   - Added `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` (frontend - ChatKit)

**Key Principles Established**:
- NO server-side session state - everything in database
- ALL MCP tools require `user_id` as first parameter
- ALL tool calls validate ownership before mutation
- Agent responses must be natural language with confirmations
- Consistent JSON format for tool responses
- Full conversation history loaded per request

**Version Bump Rationale**:
- MAJOR version (1.0.0 → 2.0.0) because:
  - Added new architectural constraint (stateless)
  - New required components (MCP server, Agents SDK, ChatKit)
  - New database schema requirements
  - Backward incompatible with Phase II (no chatbot)

## Outcome

- ✅ Impact: Constitution fully updated for Phase III with 7 core principles, stateless architecture requirements, MCP tool specifications, and comprehensive deliverable checklist
- 🧪 Tests: Manual validation passed - all placeholders filled, no bracket tokens remaining, proper version semantics
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts:
  - Create specs/ai-chatbot/spec.md (feature specification)
  - Create specs/ai-chatbot/plan.md (architecture and MCP design)
  - Create specs/ai-chatbot/tasks.md (implementation tasks)
- 🧠 Reflection: Constitution now provides clear guidance for Phase III implementation with non-negotiable rules for stateless design, MCP tool conventions, and user isolation

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution update successful
- Graders run and results (PASS/FAIL): PASS - all requirements captured
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase III with spec creation, ensuring MCP tool design aligns with constitution principles
