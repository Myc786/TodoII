---
id: 2-ai-chatbot-extension-plan
title: AI Chatbot Extension Plan
stage: plan
date: 2026-01-17
surface: agent
model: Claude Sonnet 4.5
feature: ai-chatbot-extension
branch: 005-ai-chatbot-extension
user: user
command: /sp.plan
labels: ["ai", "chatbot", "planning", "mcp", "openai"]
links:
  spec: ./spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/005-ai-chatbot-extension/plan.md
  - specs/005-ai-chatbot-extension/research.md
  - specs/005-ai-chatbot-extension/data-model.md
  - specs/005-ai-chatbot-extension/contracts/mcp-tools.yaml
  - specs/005-ai-chatbot-extension/quickstart.md
  - specs/005-ai-chatbot-extension/agent-context.md
tests: []
outcome: Implementation plan completed with all design artifacts
evaluation: Plan addresses all requirements from user input and includes comprehensive architecture
---

# AI Chatbot Extension Plan

## User Input

```
/sp.plan

Objective:
Extend the existing authenticated Todo Full-Stack Web Application
by adding an AI-powered chatbot that allows users to manage their
tasks using natural language, powered by OpenAI ChatKit, Agents SDK,
and the Official MCP SDK.

--------------------------------------------------
PHASE 1: Chatbot Architecture & Agent Design
--------------------------------------------------

1. Define a dedicated Todo Chatbot Agent
2. Assign responsibilities:
   - Understand user intent
   - Call MCP tools only
   - Never access database or APIs directly
3. Ensure agent operates strictly within authenticated user context

--------------------------------------------------
PHASE 2: Authentication & Security Context
--------------------------------------------------

4. Ensure chatbot requests include JWT token
5. Validate JWT on every chatbot interaction
6. Extract user_id from JWT and pass to MCP tools
7. Enforce strict per-user data isolation

--------------------------------------------------
PHASE 3: MCP Tool Design
--------------------------------------------------

8. Define MCP tools:
   - create_task
   - list_tasks
   - update_task
   - complete_task
   - delete_task

9. For each MCP tool:
   - Validate input parameters
   - Enforce authenticated user context
   - Reuse existing backend logic
   - Return structured responses

--------------------------------------------------
PHASE 4: Natural Language → Tool Mapping
--------------------------------------------------

10. Design system prompt for the Todo Chatbot Agent
11. Map user intents to MCP tools:
    - "Add a task…" → create_task
    - "Show my tasks" → list_tasks
    - "Mark task as complete" → complete_task
12. Handle ambiguous input with clarification questions

--------------------------------------------------
PHASE 5: Frontend Chat UI Integration
--------------------------------------------------

13. Integrate OpenAI ChatKit UI components
14. Create floating chatbot widget (bottom-right)
15. Implement expandable chat panel
16. Display message bubbles (User vs AI)
17. Show typing indicators and loading states

--------------------------------------------------
PHASE 6: Backend Integration via MCP
--------------------------------------------------

18. Connect MCP tools to FastAPI services
19. Ensure no new REST endpoints are required
20. Ensure all tool execution flows through MCP only

--------------------------------------------------
PHASE 7: Error Handling & Safety
--------------------------------------------------

21. Handle invalid or unsupported user commands
22. Handle authentication failures (401)
23. Prevent prompt injection and unsafe instructions
24. Gracefully handle tool execution errors

--------------------------------------------------
PHASE 8: UI Polish & Theme Compatibility
--------------------------------------------------

25. Ensure chatbot works in both Light and Dark themes
26. Add smooth animations and transitions
27. Ensure mobile and desktop responsiveness
```

## Response Summary

Created a comprehensive implementation plan for the AI-Powered Todo Chatbot Extension with all required artifacts:

### Plan Document (plan.md)
- Complete implementation plan with 7 phases
- Technical context and architecture overview
- Constitution check and gates validation
- Detailed tasks for each phase

### Research Document (research.md)
- MCP SDK integration patterns
- OpenAI ChatKit UI integration approaches
- Authentication context management
- Natural language understanding patterns

### Data Model (data-model.md)
- ChatMessage entity with sender, content, timestamp
- ChatSession entity for session management
- UserIntent entity for intent recognition
- MCPToolCall entity for tool execution tracking

### API Contracts (contracts/mcp-tools.yaml)
- OpenAPI specification for all MCP tools
- Request/response schemas for create_task, list_tasks, update_task, complete_task, delete_task
- Error response structures
- Authentication patterns

### Quickstart Guide (quickstart.md)
- Environment setup instructions
- Installation steps for frontend/backend
- Key integration points
- Testing procedures

### Agent Context (agent-context.md)
- Technology stack context for OpenAI ChatKit and MCP SDK
- Implementation guidelines and security requirements
- Key components to implement

The plan addresses all requirements from the user input, including:
- Dedicated Todo Chatbot Agent design
- Authentication and security context
- MCP tool design for all required operations
- Natural language to tool mapping
- Frontend UI integration
- Backend integration via MCP
- Error handling and safety mechanisms
- Theme compatibility

All deliverables have been created and the implementation plan is ready to proceed to the tasks phase (/sp.tasks).