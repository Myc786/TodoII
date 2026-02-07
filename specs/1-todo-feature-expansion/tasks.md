---
description: "Task list for Todo App Feature Expansion implementation"
---

# Tasks: Todo App Feature Expansion

**Input**: Design documents from `/specs/1-todo-feature-expansion/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app structure based on plan.md

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create feature branch 1-todo-feature-expansion
- [X] T002 Review existing codebase and document current limitations
- [X] T003 [P] Set up development environment for feature development
- [X] T004 [P] Create feature-specific documentation directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

Foundational tasks for this project:

- [X] T005 [P] Update Task model with priority, due_date, recurrence_pattern, original_task_id fields in backend/src/models/task.py
- [X] T006 [P] Create Tag model in backend/src/models/tag.py
- [X] T007 [P] Create TaskTag association model in backend/src/models/task_tag.py
- [X] T008 [P] Update TaskCreate, TaskUpdate schemas in backend/src/models/task_schemas.py
- [X] T009 Create database migration for schema changes in backend/migrations/
- [X] T010 [P] Update Task interface in frontend/src/lib/types.ts with new fields
- [X] T011 [P] Create Tag interface in frontend/src/lib/types.ts
- [X] T012 Create helper functions for working with new data structures
- [X] T013 [P] Update TaskService methods to handle priority and tags in backend/src/services/task_service.py
- [X] T014 [P] Update task CRUD operations to support new fields in backend/src/services/task_service.py
- [X] T015 [P] Add endpoints for managing tags in backend/src/api/routes/tags.py
- [X] T016 [US1] Update task creation endpoint to support tags in backend/src/api/routes/tasks.py
- [X] T017 [US1] Update task update endpoint to support tags in backend/src/api/routes/tasks.py
- [X] T018 [P] [US1] Add priority dropdown component in frontend/src/components/task/priority-selector.tsx
- [X] T019 [P] [US1] Create tag input component in frontend/src/components/task/tag-input.tsx
- [X] T020 [P] [US1] Update TaskForm component to include priority and tag inputs in frontend/src/components/task/task-form.tsx
- [X] T021 [US1] Update TaskCard component to display priority and tags in frontend/src/components/task/task-card.tsx
- [X] T022 [US1] Update TaskList component to handle tasks with priority and tags in frontend/src/components/task/task-list.tsx
- [X] T023 [US1] Implement tag management UI in frontend/src/components/task/tag-manager.tsx
- [X] T024 [US1] Add tag creation functionality in frontend/src/components/task/tag-creator.tsx
- [X] T025 [US1] Update dashboard UI to show priority and tags in frontend/src/app/dashboard/page.tsx

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 2 - Search and Filter Tasks (Priority: P1)

**Goal**: As a user, I want to search and filter my tasks by various criteria (status, priority, tags, date) so that I can quickly find the tasks I need to work on. This helps me manage large task lists efficiently.

**Independent Test**: Can be fully tested by creating multiple tasks with different attributes, then applying various search and filter combinations to verify that only matching tasks are displayed.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T026 [P] [US2] Contract test for search endpoint in backend/tests/contract/test_search.py
- [ ] T027 [P] [US2] Integration test for search and filter functionality in backend/tests/integration/test_search_filters.py

### Implementation for User Story 2

- [X] T028 [P] [US2] Implement search endpoint in backend/src/api/routes/tasks.py
- [X] T029 [US2] Implement search functionality in TaskService in backend/src/services/task_service.py
- [X] T030 [US2] Add search parameters validation in backend/src/models/task_schemas.py
- [X] T031 [US2] Update existing task listing to support filtering parameters in backend/src/api/routes/tasks.py
- [X] T032 [US2] Update TaskService to handle filtering by priority, tags, and dates in backend/src/services/task_service.py
- [X] T033 [US2] Create advanced filter component in frontend/src/components/task/task-filters.tsx
- [X] T034 [US2] Update task list to support search and filtering in frontend/src/components/task/task-list.tsx
- [X] T035 [US2] Update frontend API client to handle search parameters in frontend/src/lib/api.ts
- [X] T036 [US2] Add search input component in frontend/src/components/task/search-input.tsx
- [X] T037 [US2] Update dashboard page to integrate search and filters in frontend/src/app/dashboard/page.tsx

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 4: User Story 3 - Sort Tasks by Different Criteria (Priority: P2)

**Goal**: As a user, I want to sort my tasks by due date, priority level, or alphabetically so that I can organize my task list in the way that best suits my workflow. This helps me see the most important or urgent tasks first.

**Independent Test**: Can be fully tested by creating tasks with varying attributes and verifying that sorting options work correctly and persist when combined with filters.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T038 [P] [US3] Contract test for sort parameters in backend/tests/contract/test_sorting.py
- [ ] T039 [P] [US3] Integration test for sorting functionality in backend/tests/integration/test_sorting.py

### Implementation for User Story 3

- [X] T040 [US3] Update TaskService to support sorting by various criteria in backend/src/services/task_service.py
- [X] T041 [US3] Add sorting parameters to task listing endpoints in backend/src/api/routes/tasks.py
- [X] T042 [US3] Add sorting parameters validation in backend/src/models/task_schemas.py
- [X] T043 [US3] Create sort controls component in frontend/src/components/task/sort-controls.tsx
- [X] T044 [US3] Update task list to support sorting functionality in frontend/src/components/task/task-list.tsx
- [X] T045 [US3] Update frontend API client to handle sorting parameters in frontend/src/lib/api.ts
- [X] T046 [US3] Update dashboard to integrate sort controls in frontend/src/app/dashboard/page.tsx

**Checkpoint**: At this point, User Stories 1, 2 AND 3 should all work independently

---

## Phase 5: User Story 4 - Create Recurring Tasks (Priority: P3)

**Goal**: As a user, I want to create tasks that repeat automatically (daily, weekly, monthly) so that I don't have to manually recreate routine tasks. This saves time and ensures I don't forget recurring responsibilities.

**Independent Test**: Can be fully tested by creating recurring tasks with different intervals and verifying that new instances are generated appropriately when previous ones are completed.

### Tests for User Story 4 (OPTIONAL - only if tests requested) ⚠️

- [ ] T047 [P] [US4] Contract test for recurring task endpoints in backend/tests/contract/test_recurring.py
- [ ] T048 [P] [US4] Integration test for recurring task functionality in backend/tests/integration/test_recurring.py

### Implementation for User Story 4

- [X] T049 [US4] Implement recurring task creation endpoint in backend/src/api/routes/tasks.py
- [X] T050 [US4] Create RecurringTaskService for handling recurrence logic in backend/src/services/recurring_task_service.py
- [X] T051 [US4] Implement recurrence pattern validation in backend/src/core/validation.py
- [X] T052 [US4] Update TaskService to handle recurring task completion and generation in backend/src/services/task_service.py
- [X] T053 [US4] Add recurrence pattern to task creation/update schemas in backend/src/models/task_schemas.py
- [X] T054 [US4] Create recurrence pattern input component in frontend/src/components/task/recurrence-input.tsx
- [X] T055 [US4] Update task form to include recurrence options in frontend/src/components/task/task-form.tsx
- [X] T056 [US4] Update task card to indicate recurring tasks in frontend/src/components/task/task-card.tsx
- [X] T057 [US4] Update frontend API client to handle recurring task operations in frontend/src/lib/api.ts
- [X] T058 [US4] Update frontend types to include recurrence patterns in frontend/src/lib/types.ts

**Checkpoint**: At this point, User Stories 1, 2, 3 AND 4 should all work independently

---

## Phase 6: User Story 5 - Set Due Dates and Receive Reminders (Priority: P3)

**Goal**: As a user, I want to set due dates and times for my tasks and receive timely reminders so that I don't miss important deadlines. This helps me stay on track with my commitments.

**Independent Test**: Can be fully tested by setting due dates for tasks and verifying that reminder notifications are triggered at the appropriate times.

### Tests for User Story 5 (OPTIONAL - only if tests requested) ⚠️

- [ ] T059 [P] [US5] Contract test for reminder endpoints in backend/tests/contract/test_reminders.py
- [ ] T060 [P] [US5] Integration test for reminder functionality in backend/tests/integration/test_reminders.py

### Implementation for User Story 5

- [X] T061 [US5] Create Reminder model in backend/src/models/reminder.py
- [X] T062 [US5] Implement reminder creation endpoint in backend/src/api/routes/reminders.py
- [X] T063 [US5] Implement reminder deletion endpoint in backend/src/api/routes/reminders.py
- [X] T064 [US5] Create ReminderService for handling reminder operations in backend/src/services/reminder_service.py
- [X] T065 [US5] Add due date validation in backend/src/core/validation.py
- [X] T066 [US5] Update Task model to properly handle due dates in backend/src/models/task.py
- [X] T067 [US5] Update TaskService to handle due dates in backend/src/services/task_service.py
- [X] T068 [US5] Create reminder scheduler/background task in backend/src/services/reminder_scheduler.py
- [X] T069 [US5] Update task form to include due date picker in frontend/src/components/task/task-form.tsx
- [X] T070 [US5] Update task card to display due dates and overdue status in frontend/src/components/task/task-card.tsx
- [X] T071 [US5] Create reminder settings component in frontend/src/components/task/reminder-settings.tsx
- [X] T072 [US5] Update frontend API client to handle reminder operations in frontend/src/lib/api.ts
- [X] T073 [US5] Update frontend types to include reminder functionality in frontend/src/lib/types.ts
- [X] T074 [US5] Add browser notification handling in frontend/src/lib/notification-utils.ts

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T075 [P] Add comprehensive error handling for all new API endpoints in backend/src/api/routes/
- [ ] T076 [P] Add logging for all new features in backend/src/core/logging_config.py
- [ ] T077 [P] Add performance monitoring for search and filter operations
- [ ] T078 [P] Update documentation for all new API endpoints
- [ ] T079 Create integration tests for combined features (search + filter + sort)
- [ ] T080 [P] Add loading states and error boundaries to all new frontend components
- [ ] T081 [P] Update UI to handle edge cases (empty search results, no tags available, etc.)
- [ ] T082 [P] Add accessibility improvements to all new components
- [ ] T083 [P] Conduct performance testing with large task lists (>1000 tasks)
- [ ] T084 [P] Update README documentation with new features
- [ ] T085 [P] Create user guides for the new features
- [ ] T086 [P] Final end-to-end testing of all integrated features

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 2

```bash
# Launch all tests for User Story 2 together (if tests requested):
Task: "Contract test for search endpoint in backend/tests/contract/test_search.py"
Task: "Integration test for search and filter functionality in backend/tests/integration/test_search_filters.py"

# Launch all backend implementation for User Story 2 together:
Task: "Implement search endpoint in backend/src/api/routes/tasks.py"
Task: "Implement search functionality in TaskService in backend/src/services/task_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Priority & Tags)
4. Complete Phase 4: User Story 2 (Search & Filter)
5. **STOP and VALIDATE**: Test User Stories 1 and 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 2 (Search & Filter)
   - Developer B: User Story 3 (Sorting)
   - Developer C: User Story 4 (Recurring Tasks)
   - Developer D: User Story 5 (Reminders)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence