# Tasks: AI-Powered Todo Chatbot with Real Data Operations

## Feature Overview
Enhance the AI-powered chatbot to operate on real application data using MCP tools, with proper authentication and user isolation.

## Phase 1: Setup
Prepare the project for MCP tool integration.

- [x] T001 Create tasks file for MCP tool integration implementation
- [x] T002 Review existing MCP tools infrastructure
- [x] T003 Examine current backend chat API in src/api/routes/chat.py
- [x] T004 Verify JWT authentication system and user_id extraction

## Phase 2: Foundational
Implement foundational changes needed for MCP tool integration.

- [x] T005 Update backend chat endpoint to accept JWT validation middleware
- [x] T006 Implement user_id extraction from JWT token
- [x] T007 Verify existing MCP tools are accessible from backend
- [x] T008 Test MCP tools with user_id parameter for isolation

## Phase 3: [US1] Real Data Operations
Enable the chatbot to use MCP tools for real data operations.

- [x] T009 [US1] Implement intent recognition for create_task command
- [x] T010 [US1] Integrate create_task MCP tool into chat endpoint
- [x] T011 [US1] Implement intent recognition for list_tasks command
- [x] T012 [US1] Integrate list_tasks MCP tool into chat endpoint
- [x] T013 [US1] Implement intent recognition for update_task/complete_task command
- [x] T014 [US1] Integrate complete_task MCP tool into chat endpoint
- [x] T015 [US1] Implement intent recognition for delete_task command
- [x] T016 [US1] Integrate delete_task MCP tool into chat endpoint
- [x] T017 [US1] Test that all MCP tools respect user_id for isolation

## Phase 4: [US2] Natural Language Processing
Enhance natural language processing to map commands to MCP tools.

- [x] T018 [US2] Update LLM prompt to route commands to MCP tools
- [x] T019 [US2] Implement command parsing for "Show my tasks" → list_tasks
- [x] T020 [US2] Implement command parsing for "Add a task..." → create_task
- [x] T021 [US2] Implement command parsing for "Mark task as complete" → complete_task
- [x] T022 [US2] Implement command parsing for "Delete task..." → delete_task
- [x] T023 [US2] Test natural language command recognition accuracy

## Phase 5: [US3] Authentication & User Isolation
Ensure proper authentication and user isolation.

- [x] T024 [US3] Verify JWT token validation before MCP tool execution
- [x] T025 [US3] Test user A cannot access user B's tasks through chat
- [x] T026 [US3] Implement proper error handling for auth failures
- [x] T027 [US3] Verify all MCP tools are called with correct user_id
- [x] T028 [US3] Test cross-user data access prevention

## Phase 6: [US4] Frontend Integration
Update frontend to work with real data operations.

- [x] T029 [US4] Update frontend API client to handle real data responses
- [x] T030 [US4] Test that chat responses reflect actual database changes
- [x] T031 [US4] Implement loading states for MCP tool execution
- [x] T032 [US4] Verify real-time state reflection in chat UI
- [x] T033 [US4] Test error handling for MCP tool failures

## Phase 7: [US5] Testing & Validation
Comprehensive testing of real data operations.

- [x] T034 [US5] Test "Show my tasks" returns actual database tasks
- [x] T035 [US5] Test "Add a task..." creates actual database entry
- [x] T036 [US5] Test "Mark task as complete" updates actual database
- [x] T037 [US5] Test "Delete task..." removes actual database entry
- [x] T038 [US5] Verify all operations maintain user isolation
- [x] T039 [US5] Performance test with MCP tool integration

## Phase 8: Polish & Cross-Cutting Concerns
Final touches and cross-cutting concerns.

- [x] T040 Test chatbot functionality across all authenticated pages
- [x] T041 Verify performance impact is acceptable (<5% degradation)
- [x] T042 Test error handling with MCP tool failures
- [x] T043 Validate user isolation with multiple user accounts
- [x] T044 Clean up any debug code or temporary implementations
- [x] T045 Document the MCP tool integration for future maintenance

## Dependencies
- User Story 1 (Real Data Operations) must be completed before User Stories 2-5 can be fully tested
- Foundational tasks (Phase 2) must be completed before any user story tasks

## Parallel Execution Opportunities
- [US2] Natural language processing tasks can run in parallel with [US3] Authentication tasks
- [US4] Frontend integration tasks can run in parallel with [US5] Testing tasks
- Testing tasks across different user stories can run in parallel

## Implementation Strategy
- MVP: Complete Phase 1-3 to deliver basic real data functionality (create/list tasks)
- Incremental delivery: Add remaining operations in priority order
- Each phase should result in a testable increment