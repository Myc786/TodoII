---
id: 3
title: AI Chatbot Architecture Decision Records
stage: general
date: 2026-02-06
surface: agent
model: claude-sonnet-4-5
feature: 1-ai-chatbot
branch: 001-ai-chatbot
user: system
command: create adr
labels: ["adr", "architecture", "cohere", "stateless", "database", "tool-calls"]
links:
  spec: specs/1-ai-chatbot/spec.md
  ticket: null
  adr: history/adr/001-cohere-via-openai-compatibility.md, history/adr/002-stateless-server-design.md, history/adr/003-tool-call-storage-json-column.md
  pr: null
files:
  - history/adr/001-cohere-via-openai-compatibility.md
  - history/adr/002-stateless-server-design.md
  - history/adr/003-tool-call-storage-json-column.md
tests:
  - ADR significance validation (impact, alternatives, scope)
  - Decision rationale completeness check
---

## Prompt

```text
creat adr
```

## Response snapshot

Created 3 Architecture Decision Records (ADRs) documenting key architectural decisions for the AI Chatbot feature.

**ADR-001: Use Cohere via OpenAI Compatibility Instead of Direct Cohere SDK**

- **Decision**: Use OpenAI Agents SDK configured with Cohere models via OpenAI Compatibility API
- **Context**: Need agent framework with tool calling for natural language task management through MCP tools
- **Rationale**:
  - OpenAI Agents SDK provides production-ready agent orchestration (vs. building custom agent loop)
  - OpenAI-compatible API is industry standard, enabling future LLM provider switches
  - Maintains Cohere cost benefits while gaining mature agent runtime
  - Indirection cost minimal (~50ms) compared to model inference (1-3s)
- **Alternatives Rejected**:
  - Direct Cohere SDK + Custom Agent Loop (too much custom code)
  - LangChain + Cohere SDK (over-engineered, heavyweight)
  - OpenAI Native Models (higher cost, constitution specifies Cohere)
  - Anthropic Claude + Custom Agent (same custom agent loop problems)
- **Trade-offs**: API indirection layer vs. mature agent runtime and standard interface

**ADR-002: Stateless Server Design with Full History Reload Per Request**

- **Decision**: Implement fully stateless server with conversation history loaded from PostgreSQL on every chat request
- **Context**: Need conversation context for AI agent while supporting horizontal scaling, server restarts, zero in-memory state
- **Rationale**:
  - Database query performance sufficient (~100ms for 100 messages vs. 1-3s LLM inference)
  - Typical conversations are short (10-30 messages)
  - Horizontal scaling works with simple round-robin load balancing
  - Zero state loss on server restart
  - Aligns with existing Phase II stateless API design
- **Alternatives Rejected**:
  - In-Memory Sessions (sticky sessions, state loss on restart, no horizontal scaling)
  - Redis Session Cache (operational complexity, premature optimization)
  - Hybrid Approach (complexity without clear benefit)
- **Trade-offs**: Higher database load vs. architectural simplicity and operational reliability
- **Performance Optimization**: Database indexes on (conversation_id, created_at), (user_id) for < 1s query time

**ADR-003: Store Tool Calls as JSON String vs Separate Table**

- **Decision**: Store MCP tool call information as JSON string in `tool_calls` column of messages table
- **Context**: Need to track which tools were executed for debugging, audit trails, and potential UI display
- **Rationale**:
  - Tool calls always retrieved with parent message (natural grouping)
  - Simpler schema with no JOINs for conversation history
  - Sufficient for current requirements (debugging, UI display, not analytics)
  - Flexible JSON structure allows adding fields without migrations
  - YAGNI principle - building for hypothetical analytics queries is premature
- **Alternatives Rejected**:
  - Separate tool_calls Table (increased query complexity, unnecessary JOINs)
  - JSONB Column (TEXT sufficient, more portable, easy to migrate later if needed)
  - No Tool Call Storage (UI and debugging requirements need tool call data)
- **Trade-offs**: No individual tool call queries vs. simpler schema and faster conversation history loads
- **Future Migration**: Can add analytics table, migrate to JSONB, or extract to data warehouse if needed

**ADR Quality Validation**:

All 3 ADRs pass significance checklist:
- ✅ **Impact**: Long-term consequences for architecture, scalability, data model
- ✅ **Alternatives**: Multiple viable options considered with detailed trade-off analysis
- ✅ **Scope**: Cross-cutting concerns affecting deployment, scaling, tool integration, database design

**Documentation Structure**:

Each ADR includes:
- Status (Accepted), Date, Feature, Context
- Decision with technical implementation details
- Positive and negative consequences
- Alternatives considered with rejection rationale
- References to spec, plan, related ADRs, constitution
- Implementation checkpoints tied to tasks.md
- Future considerations and migration paths

## Outcome

- ✅ Impact: 3 comprehensive ADRs documenting foundational architectural decisions for AI chatbot feature with detailed rationale, alternatives analysis, and implementation guidance
- 🧪 Tests: All ADRs pass significance validation (impact, alternatives, scope). Decision rationale complete with trade-off analysis.
- 📁 Files: 3 ADRs created in history/adr/ directory (001-cohere, 002-stateless, 003-tool-calls)
- 🔁 Next prompts: Reference ADRs during implementation (Phases 2-3 in tasks.md). Update ADRs if architectural decisions change during development. Create additional ADRs for any new significant decisions.
- 🧠 Reflection: ADRs successfully capture key architectural trade-offs and provide clear rationale for future reference. Each ADR addresses different concern (LLM integration, state management, data model) with comprehensive alternatives analysis. Implementation checkpoints linked to tasks.md ensure ADR decisions are validated during execution.

## Evaluation notes (flywheel)

- Failure modes observed: None - all 3 ADRs successfully created with complete rationale and alternatives analysis
- Graders run and results (PASS/FAIL): PASS - All ADRs meet significance criteria (impact, alternatives, scope). Decision rationale comprehensive. Implementation guidance clear.
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin Phase 0 research to validate ADR-001 assumptions (Cohere compatibility API supports function calling with MCP tools) and ADR-002 assumptions (database query performance < 1s for 100 messages)
