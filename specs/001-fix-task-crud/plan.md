# Implementation Plan: Fix Task CRUD Operations

**Branch**: `001-fix-task-crud` | **Date**: 2026-02-07 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-fix-task-crud/spec.md`

## Summary

Fix task Edit, Complete, and Delete operations that fail to persist changes to the backend. **Root cause identified**: The delete handler in the dashboard only updates local state without calling the backend API. Update and toggle operations are correctly implemented but require verification.

**Approach**: Single-file fix in `frontend/src/app/dashboard/page.tsx` to make `handleTaskDeleted` call `apiClient.deleteTask()` before updating local state.

## Technical Context

**Language/Version**: TypeScript 5.x (Frontend), Python 3.11 (Backend)
**Primary Dependencies**: Next.js 14, React 18, FastAPI, SQLModel
**Storage**: Neon Serverless PostgreSQL
**Testing**: Manual verification (existing patterns, minimal change)
**Target Platform**: Web (Vercel + Hugging Face Spaces)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: UI updates within 500ms after mutation
**Constraints**: No breaking changes to task creation, same API URLs
**Scale/Scope**: Single file change, ~15 lines modified

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| Spec-Driven Development | ✅ Pass | Feature has spec.md |
| Security First | ✅ Pass | No auth changes, uses existing JWT |
| Tech Stack Adherence | ✅ Pass | No new dependencies |
| Stateless Architecture | ✅ Pass | No server state changes |
| Smallest Viable Diff | ✅ Pass | Single function fix |

**Gate Result**: PASS - Proceed with implementation.

## Project Structure

### Documentation (this feature)

```text
specs/001-fix-task-crud/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Investigation findings
├── data-model.md        # Data model (no changes needed)
├── quickstart.md        # Implementation guide
├── contracts/           # API contracts (existing, no changes)
│   └── task-crud-api.yaml
├── checklists/
│   └── requirements.md  # Quality checklist
└── tasks.md             # Implementation tasks (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/routes/tasks.py     # Task endpoints (no changes needed)
│   ├── models/task.py          # Task model (no changes needed)
│   ├── services/task_service.py # Task service (no changes needed)
│   └── main.py                  # CORS config (no changes needed)
└── tests/

frontend/
├── src/
│   ├── app/dashboard/page.tsx  # 🔧 FIX: handleTaskDeleted
│   ├── components/task/        # Task components (no changes needed)
│   └── lib/api.ts              # API client (no changes needed)
└── tests/
```

**Structure Decision**: Web application structure. Only `frontend/src/app/dashboard/page.tsx` requires modification.

## Complexity Tracking

> No violations - this is a minimal bug fix.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | - | - |

## Implementation Phases

### Phase 1: Fix Delete Handler (P1)

**Objective**: Make delete operations persist to backend

**Changes**:

1. **frontend/src/app/dashboard/page.tsx**
   - Rename `handleTaskDeleted` to `handleTaskDelete`
   - Make it async and call `apiClient.deleteTask(taskId)`
   - Add error handling matching existing patterns
   - Update `onDelete` prop to use new handler

**Before** (lines 59-61):
```typescript
const handleTaskDeleted = (deletedTaskId: string) => {
  setTasks(prev => prev.filter(task => task.id !== deletedTaskId));
};
```

**After**:
```typescript
const handleTaskDelete = async (taskId: string) => {
  try {
    const response = await apiClient.deleteTask(taskId);
    if (response.success) {
      setTasks(prev => prev.filter(task => task.id !== taskId));
    } else {
      console.error('Failed to delete task:', response.error);
    }
  } catch (error) {
    console.error('Failed to delete task:', error);
  }
};
```

**Line 199** change:
```typescript
// Before
onDelete={handleTaskDeleted}
// After
onDelete={handleTaskDelete}
```

### Phase 2: Verification Testing (P1)

**Objective**: Verify all CRUD operations work correctly

**Test Cases**:

| # | Operation | Steps | Expected Result |
|---|-----------|-------|-----------------|
| 1 | Delete | Create task → Delete → Refresh | Task does NOT reappear |
| 2 | Edit | Create task → Edit title → Refresh | Title persists |
| 3 | Toggle | Create task → Toggle complete → Refresh | Status persists |
| 4 | Create | Create task → Refresh | Task persists (regression check) |
| 5 | Error | Delete non-existent task | Error logged, no crash |

### Phase 3: Deployment (P2)

**Objective**: Deploy verified fixes to production

**Steps**:

1. **Frontend deployment** (Vercel):
   - Commit and push to main branch
   - Vercel auto-deploys
   - Verify production at Vercel URL

2. **Backend verification** (Hugging Face Spaces):
   - No backend changes required
   - Verify backend still operational at HF Spaces URL

3. **Production validation**:
   - Run test cases 1-5 on production
   - Check browser Network tab for successful requests
   - Verify no CORS errors in console

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Other components use broken pattern | Low | Medium | Search codebase for similar `onDelete` patterns |
| Regression in task creation | Low | High | Test case #4 verifies |
| Deployment failure | Low | Medium | Vercel rollback if needed |

## Success Criteria Mapping

| Spec Criteria | Implementation |
|---------------|----------------|
| SC-001: Edit operations succeed | Phase 2, Test #2 |
| SC-002: Toggle operations succeed | Phase 2, Test #3 |
| SC-003: Delete operations succeed | Phase 1 fix + Phase 2, Test #1 |
| SC-004: UI updates within 500ms | Existing optimistic update pattern |
| SC-005: Zero CORS errors | Phase 2 verification |
| SC-006: Changes persist on refresh | Phase 2, Tests #1-3 |
| SC-007: Create still works | Phase 2, Test #4 |
| SC-008: Error messages shown | Phase 1 error handling |

## Dependencies

- [x] Spec complete: `specs/001-fix-task-crud/spec.md`
- [x] Research complete: `specs/001-fix-task-crud/research.md`
- [x] API contracts documented: `specs/001-fix-task-crud/contracts/task-crud-api.yaml`
- [ ] Implementation: Run `/sp.tasks` to generate task breakdown

## Next Steps

Run `/sp.tasks` to generate the implementation task list, then proceed with the fix.
