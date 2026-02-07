# Tasks: Fix Task CRUD Operations

**Input**: Design documents from `/specs/001-fix-task-crud/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, data-model.md ✓, contracts/ ✓

**Tests**: Not explicitly requested - verification is manual per plan.md

**Organization**: Tasks grouped by user story for independent verification.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1-US4)
- File paths are relative to repository root

## Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| Phase 1: Pre-flight | 2 | Verify current state |
| Phase 2: Fix | 2 | Implement the fix |
| Phase 3: US1 Verify Edit | 1 | Verify edit works |
| Phase 4: US2 Verify Toggle | 1 | Verify toggle works |
| Phase 5: US3 Verify Delete | 1 | Verify delete works (THE FIX) |
| Phase 6: US4 Verify CORS | 1 | Verify no CORS errors |
| Phase 7: Deployment | 3 | Deploy and validate |
| **Total** | **11** | |

---

## Phase 1: Pre-flight Verification

**Purpose**: Confirm current state and reproduce the bug before fixing

- [ ] T001 Verify backend is running and accessible at configured API URL
- [ ] T002 Reproduce delete bug: create task → delete → refresh → confirm task reappears

**Checkpoint**: Bug confirmed - proceed with fix

---

## Phase 2: Implement Fix

**Purpose**: Fix the delete handler in dashboard to call the backend API

**File to modify**: `frontend/src/app/dashboard/page.tsx`

- [x] T003 Replace `handleTaskDeleted` function (lines 59-61) with async `handleTaskDelete` that calls `apiClient.deleteTask()` in `frontend/src/app/dashboard/page.tsx`
- [x] T004 Update `onDelete` prop (line 199) from `handleTaskDeleted` to `handleTaskDelete` in `frontend/src/app/dashboard/page.tsx`

**Code Change for T003**:
```typescript
// Replace lines 59-61:
const handleTaskDeleted = (deletedTaskId: string) => {
  setTasks(prev => prev.filter(task => task.id !== deletedTaskId));
};

// With:
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

**Code Change for T004**:
```typescript
// Line 199 - Change:
onDelete={handleTaskDeleted}
// To:
onDelete={handleTaskDelete}
```

**Checkpoint**: Code fix complete - proceed with verification

---

## Phase 3: User Story 1 - Edit Task (Priority: P1)

**Goal**: Verify edit operations persist to backend

**Independent Test**: Create task → Edit title → Refresh → Title persists

- [ ] T005 [US1] Manually verify: Edit a task title and confirm it persists after page refresh

**Acceptance Criteria**:
- [ ] Task title updates immediately in UI
- [ ] After refresh, edited title is still displayed
- [ ] No errors in browser console

**Checkpoint**: Edit functionality verified ✓

---

## Phase 4: User Story 2 - Mark Task Complete/Incomplete (Priority: P1)

**Goal**: Verify toggle operations persist to backend

**Independent Test**: Create task → Toggle complete → Refresh → Status persists

- [ ] T006 [US2] Manually verify: Toggle task completion and confirm it persists after page refresh

**Acceptance Criteria**:
- [ ] Task completion status updates immediately in UI
- [ ] After refresh, completion status is preserved
- [ ] Toggling back to incomplete also persists

**Checkpoint**: Toggle functionality verified ✓

---

## Phase 5: User Story 3 - Delete Task (Priority: P2) 🎯 THE FIX

**Goal**: Verify delete operations NOW persist to backend (after fix)

**Independent Test**: Create task → Delete → Refresh → Task does NOT reappear

- [ ] T007 [US3] Manually verify: Delete a task and confirm it does NOT reappear after page refresh

**Acceptance Criteria**:
- [ ] Task is removed from UI immediately on delete
- [ ] After refresh, deleted task does NOT reappear
- [ ] Browser Network tab shows DELETE request with 200 status
- [ ] No errors in browser console

**Checkpoint**: Delete functionality verified ✓ (This confirms the fix works)

---

## Phase 6: User Story 4 - CORS Preflight Success (Priority: P1)

**Goal**: Verify no CORS errors occur during any operation

**Independent Test**: Open browser console → Perform all CRUD operations → No CORS errors

- [x] T008 [US4] Manually verify: No CORS errors in browser console during edit, toggle, and delete operations

**Acceptance Criteria**:
- [ ] No "Access-Control-Allow-Origin" errors
- [ ] No "preflight request" failures
- [ ] All operations complete without network errors

**Checkpoint**: CORS verification complete ✓

---

## Phase 7: Deployment & Production Validation

**Purpose**: Deploy fix and validate in production environment

- [x] T009 Commit fix with message: "fix: task delete now calls backend API before updating state"
- [x] T010 Push to main branch and verify Vercel deployment succeeds
- [ ] T011 Run full verification suite on production (repeat T005-T008 on production URL)

**Acceptance Criteria**:
- [ ] Vercel deployment completes without errors
- [ ] Production URL accessible
- [ ] All CRUD operations work in production
- [ ] Task creation still works (regression check)

**Checkpoint**: Production deployment complete and validated ✓

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Pre-flight)
    ↓
Phase 2 (Fix)
    ↓
┌───┴───┬───────┬───────┐
↓       ↓       ↓       ↓
Phase 3 Phase 4 Phase 5 Phase 6   (All verification can be parallel)
(US1)   (US2)   (US3)   (US4)
└───┬───┴───────┴───────┘
    ↓
Phase 7 (Deployment)
```

### Critical Path

1. **T001-T002**: Confirm bug exists
2. **T003-T004**: Apply fix (SINGLE FILE CHANGE)
3. **T007**: Verify delete now works (VALIDATES THE FIX)
4. **T009-T011**: Deploy and confirm production

### Parallel Opportunities

After Phase 2 completes:
- T005 (US1 Edit), T006 (US2 Toggle), T007 (US3 Delete), T008 (US4 CORS) can all run in parallel
- These are independent verification tasks that don't modify code

---

## Implementation Strategy

### MVP Scope

**Minimum Viable Fix**: T003 + T004 + T007
- Just the code change and delete verification
- This is sufficient to resolve the reported bug

### Full Verification Scope

All tasks T001-T011 for complete validation including:
- Pre-flight bug confirmation
- All user story verification
- Production deployment

### Time Estimate

This is a minimal fix:
- 1 file modified
- ~15 lines of code changed
- 11 tasks total (most are verification, not implementation)

---

## Files Changed

| File | Change Type | Tasks |
|------|-------------|-------|
| `frontend/src/app/dashboard/page.tsx` | Modify | T003, T004 |

**No backend changes required** - all backend endpoints and CORS are already correctly implemented.
