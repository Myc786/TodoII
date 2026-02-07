<!-- SYNC IMPACT REPORT:
Version change: 1.0.0 → 2.0.0
Modified principles:
- Security First Architecture → expanded with MCP user_id validation
- Tech Stack Adherence → Phase III additions (OpenAI Agents SDK, MCP, ChatKit)
- Added: Stateless Architecture Principle
- Added: MCP Tool Design Principle
- Added: AI Agent Behavior Principle
Added sections: Phase III: AI Chatbot Integration
Removed sections: Zero Manual Coding Enforcement (superseded by Spec-Driven Development)
Templates requiring updates:
- .specify/templates/spec-template.md ✅ needs AI chatbot section
- .specify/templates/plan-template.md ✅ needs MCP/agent planning guidance
- .specify/templates/tasks-template.md ✅ needs tool/agent task types
- README.md ⚠ pending Phase III update
Follow-up TODOs:
- Create MCP tool specifications in specs/ai-chatbot/
- Document OpenAI domain key setup for production
-->

# Todo Application with AI Chatbot Constitution

**Version**: 2.0.0
**Ratification Date**: 2026-02-05
**Last Amended**: 2026-02-06
**Project**: Full-Stack Todo Application with Natural Language AI Interface (Phase III)

## Project Overview

A production-ready todo management application with natural language AI interface, built using:
- **Frontend**: Next.js 14+ with OpenAI ChatKit for AI chat UI
- **Backend**: FastAPI with OpenAI Agents SDK for AI logic
- **AI Integration**: Model Context Protocol (MCP) for tool exposure
- **Database**: Neon Serverless PostgreSQL with SQLModel ORM
- **Authentication**: Better Auth with JWT tokens
- **Deployment**: Vercel (frontend) + Hugging Face Spaces (backend)

## Core Principles

### 1. Spec-Driven Development (NON-NEGOTIABLE)

**Principle**: All implementation MUST follow the Agentic Dev Stack workflow: spec → plan → tasks → implement.

**Rules**:
- Every feature begins with a specification in `specs/<feature>/spec.md`
- NO manual coding without referencing spec files via `@specs/` syntax
- All changes MUST be traceable to specific spec documents
- Architecture decisions MUST be documented in ADRs when significant
- Use CLAUDE.md files for runtime development guidance at root/frontend/backend levels

**Rationale**: Ensures reproducibility, traceability, and prevents scope creep. Critical for evaluation and handoff.

### 2. Stateless Architecture (Phase III Requirement)

**Principle**: Backend MUST maintain NO server-side session memory. All conversation state resides in database.

**Rules**:
- NO in-memory state for conversations, message history, or agent context
- Every `/api/chat` request MUST reload full conversation history from database
- Conversation state stored in: `conversations` table (metadata) + `messages` table (content)
- Agent MUST be re-initialized per request with full message history
- Frontend MUST persist `conversation_id` (localStorage or URL parameter) for resumption

**Rationale**: Enables horizontal scaling, crash recovery, and multi-instance deployment without sticky sessions.

### 3. Security First Architecture

**Principle**: 100% user isolation with JWT-based authentication on every operation.

**Rules**:
- Authentication via Better Auth (frontend) → JWT tokens → FastAPI verification (backend)
- ALL API endpoints MUST verify JWT and extract `user_id`
- ALL database queries MUST filter by authenticated `user_id`
- ALL MCP tool calls MUST require `user_id` as first mandatory parameter
- ALL tool executions MUST validate ownership (`task.user_id == provided_user_id`)
- JWT secret MUST be shared via `BETTER_AUTH_SECRET` environment variable
- NO data leakage between users - return 403 for unauthorized access attempts
- `/api/chat` endpoint MUST extract `user_id` from JWT, not URL parameter

**Rationale**: Multi-tenant isolation is fundamental. Tools exposed to AI MUST be user-scoped to prevent data leaks.

### 4. MCP Tool Design (Phase III Critical)

**Principle**: AI tools MUST be exposed via official MCP SDK with strict conventions.

**Rules**:
- Tool names MUST match specification exactly: `add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`
- ALL tools MUST accept `user_id: str` as first/mandatory parameter
- Tool responses MUST use consistent format:
  ```python
  # Single task: {"task_id": int, "status": str, "title": str, ...}
  # Multiple tasks: [{"task_id": int, ...}, ...]
  ```
- Tools MUST validate ownership before ANY mutation
- Tools MUST return human-readable error messages on failure
- MCP server MUST use official transports (stdio/http/sse - prefer stdio for simplicity)
- NO tools may access database without `user_id` filtering

**Rationale**: MCP protocol ensures AI-safe tool exposure. Consistent format enables reliable agent chaining.

### 5. AI Agent Behavior (Phase III)

**Principle**: Agent MUST use OpenAI Agents SDK with natural language confirmation and graceful error handling.

**Rules**:
- Agent MUST chain tools when needed (e.g., `list_tasks` → `delete_task`)
- Agent MUST confirm actions in natural language: "Task 'Buy groceries' added successfully!"
- Agent MUST handle errors gracefully: "I couldn't find task #99 – maybe check the list?"
- Agent MUST NOT invent tasks or data not returned by tools
- Agent responses MUST be stored in `messages` table with `role='assistant'`
- Tool call results MUST be logged for debugging but NOT shown verbatim to user
- Agent MUST receive full conversation history (not just last N messages)

**Rationale**: Natural language UX requires confirmations and graceful failures. Tool chaining enables complex workflows.

### 6. Tech Stack Adherence (Fixed - Phase III)

**Principle**: Use ONLY the approved Phase III technology stack. NO substitutions without constitution amendment.

**Stack**:
- **Frontend UI**: Next.js 14+ App Router, React Server Components, Tailwind CSS
- **AI Chat UI**: OpenAI ChatKit (React component library)
- **Backend API**: FastAPI (Python 3.11+), Uvicorn server
- **AI Logic**: OpenAI Agents SDK (official Python SDK for agent/runner)
- **Tool Protocol**: Model Context Protocol (MCP) - official SDK
- **ORM**: SQLModel (Pydantic v2 + SQLAlchemy)
- **Database**: Neon Serverless PostgreSQL
- **Auth**: Better Auth (frontend) + JWT verification (backend)
- **Deployment**: Vercel (frontend), Hugging Face Spaces (backend)

**Database Schema** (MUST match exactly):
```sql
-- Existing tables
users (id UUID PK, email, name, password, created_at, updated_at)
tasks (id UUID PK, user_id UUID FK, title, description, completed BOOL,
       priority, due_date, recurrence_pattern, version INT, created_at, updated_at)

-- Phase III additions
conversations (id UUID PK, user_id UUID FK, created_at, updated_at)
messages (id UUID PK, user_id UUID FK, conversation_id UUID FK,
          role ENUM('user', 'assistant', 'system'), content TEXT,
          tool_calls JSON, created_at)
```

**ChatKit Configuration**:
- Production: Use domain allowlist with `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`
- Development: localhost allowed by default
- Handle streaming responses if supported
- Show loading/thinking states during tool execution

**Rationale**: Fixed stack ensures consistency, evaluation fairness, and avoids choice paralysis.

### 7. Conversation Flow (Stateless Implementation)

**Principle**: Every chat request MUST follow the stateless conversation protocol.

**Flow**:
1. **Extract JWT** → Verify → Get `user_id`
2. **Load conversation history**:
   ```sql
   SELECT role, content, tool_calls, created_at
   FROM messages
   WHERE conversation_id = ? AND user_id = ?
   ORDER BY created_at ASC
   ```
3. **Append new user message** → Store in `messages` table
4. **Initialize agent** with full message history + MCP tools
5. **Run agent** → Get response + tool calls
6. **Store assistant response** in `messages` table
7. **Return** `{conversation_id, response, tool_calls?}` to frontend

**Endpoint**: `POST /api/chat` (NOT `/api/{user_id}/chat` - user_id from JWT)

**Request**:
```json
{
  "conversation_id": "uuid-or-null",  // null = new conversation
  "message": "Add a task to buy groceries"
}
```

**Response**:
```json
{
  "conversation_id": "uuid",
  "response": "Task 'Buy groceries' added successfully!",
  "tool_calls": [
    {"tool": "add_task", "args": {"user_id": "...", "title": "Buy groceries"}}
  ]
}
```

**Rationale**: Explicit flow prevents state bugs. Storing tool_calls enables debugging and audit trails.

## Code Quality Standards

### Python (Backend)

**Requirements**:
- Type hints everywhere: `def add_task(user_id: str, title: str) -> Task:`
- Pydantic v2 models for all request/response schemas
- Black + Ruff for formatting and linting
- HTTPException for all API errors with proper status codes
- APIRouter for modular endpoint organization
- Depends() for JWT auth and DB session injection
- Structured logging for agent steps, tool calls, errors

**Example**:
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

router = APIRouter()

@router.post("/chat")
async def chat_endpoint(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),  # JWT extraction
    db: Session = Depends(get_session)
):
    # Load conversation, run agent, store messages
    ...
```

### TypeScript (Frontend)

**Requirements**:
- Strict TypeScript mode enabled
- Server Components by default, Client Components only when needed
- ChatKit integration with proper typing
- localStorage for conversation_id persistence
- Error boundaries for chat UI failures
- Loading states during agent thinking

### MCP Server

**Requirements**:
- Use official MCP SDK (Python)
- Prefer stdio transport for simplicity
- Document each tool with clear docstrings
- Validate all inputs before database access
- Return consistent JSON format
- Log all tool calls with user_id and timestamp

## Testing & Validation

**Required Tests**:
- Tool ownership validation (403 when user_id mismatch)
- Conversation loading with correct user_id filtering
- JWT expiration and invalid token handling
- Agent tool chaining (list → delete scenario)
- Stateless behavior (restart server mid-conversation)

**Manual Testing Checklist**:
- [ ] Chat UI loads and shows conversation history
- [ ] "Add task: Buy milk" creates task in database
- [ ] "List my tasks" shows only user's tasks
- [ ] "Complete task #X" updates correct task
- [ ] "Delete task #X" requires confirmation and deletes
- [ ] Conversation persists after page refresh
- [ ] Two users in separate sessions see different tasks
- [ ] Invalid JWT returns 401

## Deliverable Checklist (Phase III)

**Completion Criteria**:
- [ ] Working stateless `/api/chat` endpoint
- [ ] MCP server exposing 5 Todo tools (`add_task`, `list_tasks`, `complete_task`, `delete_task`, `update_task`)
- [ ] Conversations + messages tables in Neon database
- [ ] OpenAI Agents SDK integration with tool chaining
- [ ] ChatKit UI integrated in frontend
- [ ] JWT authentication on every chat request
- [ ] All tools validate `user_id` and ownership
- [ ] Natural language confirmations for actions
- [ ] Graceful error handling in agent responses
- [ ] Conversation history persistence and loading
- [ ] Demo video showing end-to-end workflow
- [ ] README with Phase III setup instructions
- [ ] All specs/plans/tasks in `specs/ai-chatbot/` directory

## Governance

**Amendment Process**:
1. Identify principle change (addition/removal/modification)
2. Determine version bump (MAJOR for breaking changes, MINOR for additions, PATCH for clarifications)
3. Update `.specify/memory/constitution.md` with Sync Impact Report
4. Update affected templates in `.specify/templates/`
5. Commit with message: `docs: amend constitution to vX.Y.Z (description)`

**Version Semantics**:
- **MAJOR** (X.0.0): Backward incompatible changes (remove principles, change stack)
- **MINOR** (X.Y.0): New principles, sections, or material expansions
- **PATCH** (X.Y.Z): Clarifications, typo fixes, non-semantic refinements

**Compliance**:
- All PRs MUST reference this constitution
- Spec reviews MUST verify alignment with principles
- Code reviews MUST check: JWT validation, user_id filtering, stateless design
- Deployment MUST set all required environment variables

**Supersedence**:
- This constitution supersedes all other development practices
- CLAUDE.md files provide runtime guidance but MUST NOT contradict constitution
- In case of conflict, constitution wins - update CLAUDE.md to align

**Critical Environment Variables** (MUST be set):
```env
# Backend (HF Spaces)
DATABASE_URL=postgresql://...
BETTER_AUTH_SECRET=...
ENVIRONMENT=production
FRONTEND_URL=https://...
OPENAI_API_KEY=sk-...

# Frontend (Vercel)
NEXT_PUBLIC_API_URL=https://...
NEXT_PUBLIC_BETTER_AUTH_URL=https://.../api/auth
NEXT_PUBLIC_BETTER_AUTH_SECRET=... (same as backend)
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=... (for ChatKit production)
```

## References

- **Spec Directory**: `specs/ai-chatbot/` (Phase III specifications)
- **MCP Documentation**: https://modelcontextprotocol.io
- **OpenAI Agents SDK**: https://github.com/openai/openai-agents-sdk-python
- **ChatKit Documentation**: https://platform.openai.com/docs/chatkit
- **Current Deployment**:
  - Frontend: https://frontend-mocha-beta-73.vercel.app
  - Backend: https://myc786-part2.hf.space
  - Database: Neon PostgreSQL (connection in HF Spaces secrets)

---

**Last Updated**: 2026-02-06
**Constitution Custodian**: Project maintainers
**Review Cycle**: Before each major phase (Phase I → Phase II → Phase III)
