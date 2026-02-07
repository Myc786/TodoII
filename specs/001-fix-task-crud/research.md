# Research: Fix Task CRUD Operations

**Feature**: 001-fix-task-crud
**Date**: 2026-02-07
**Status**: Complete

## Executive Summary

Investigation complete. **One critical bug identified** causing delete operations to fail. Update and toggle operations appear correctly implemented but require verification testing.

## Key Findings

### 1. Root Cause: Delete Operation Bug

**Location**: `frontend/src/app/dashboard/page.tsx` (lines 59-61, 199)

**Problem**: The `handleTaskDeleted` function passed to `TaskList.onDelete` prop only removes the task from local React state. It does NOT call the `apiClient.deleteTask()` API method.

```typescript
// Current (BROKEN) - Line 59-61
const handleTaskDeleted = (deletedTaskId: string) => {
  setTasks(prev => prev.filter(task => task.id !== deletedTaskId));
};

// Line 199: Passing broken handler
onDelete={handleTaskDeleted}
```

**Result**:
- UI shows task as deleted ✓
- Backend database unchanged ✗
- Task reappears on page refresh ✗

**Fix Required**: Create async handler that calls `apiClient.deleteTask()` before updating state.

### 2. Backend API Status

All endpoints are correctly implemented in `backend/src/api/routes/tasks.py`:

| Method | Route | Status | Lines |
|--------|-------|--------|-------|
| PUT | `/{task_id}` | ✅ Implemented | 114-161 |
| DELETE | `/{task_id}` | ✅ Implemented | 164-194 |
| PATCH | `/{task_id}/toggle` | ✅ Implemented | 197-230 |

### 3. Frontend API Client Status

All methods correctly implemented in `frontend/src/lib/api.ts`:

| Method | API Function | Status | Lines |
|--------|--------------|--------|-------|
| PUT | `updateTask()` | ✅ Correct | 119-145 |
| DELETE | `deleteTask()` | ✅ Correct | 177-201 |
| PATCH | `toggleTaskCompletion()` | ✅ Correct | 148-174 |

### 4. CORS Configuration Status

**Location**: `backend/src/main.py` (lines 44-50)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],  # All methods including PUT, PATCH, DELETE
    allow_headers=["*"],
)
```

**Status**: ✅ Correctly configured - allows all HTTP methods including PUT, PATCH, DELETE, OPTIONS.

### 5. Dashboard Handler Analysis

| Operation | Handler | Calls API? | Status |
|-----------|---------|------------|--------|
| Update | `handleTaskUpdate` | ✅ Yes | Works |
| Toggle | `handleTaskToggle` | ✅ Yes | Works |
| Delete | `handleTaskDeleted` | ❌ No | **BROKEN** |

## Decisions

### Decision 1: Fix Delete Handler Pattern

**Chosen Approach**: Follow the same pattern as `handleTaskToggle` and `handleTaskUpdate`

**Rationale**:
- Consistent with existing codebase patterns
- Uses existing `apiClient.deleteTask()` method
- Minimal code change (single function update)

**Alternatives Rejected**:
- Refactoring to use React Query/SWR: Out of scope, adds new dependency
- Global state management: Overkill for this fix

### Decision 2: Error Handling for Delete

**Chosen Approach**: Add try/catch with console.error, matching existing handlers

**Rationale**: Matches `handleTaskToggle` and `handleTaskUpdate` error handling patterns

## Files to Modify

| File | Change | Priority |
|------|--------|----------|
| `frontend/src/app/dashboard/page.tsx` | Fix `handleTaskDeleted` to call API | P1 |

## Verification Tests Required

1. **Delete Task**: Create task → Delete → Refresh page → Task should NOT reappear
2. **Edit Task**: Create task → Edit title → Refresh → Title should persist
3. **Toggle Complete**: Create task → Toggle → Refresh → Status should persist
4. **Error Handling**: Test with invalid task ID → Should show error message

## Risks

1. **Low Risk**: Other components might also use the broken pattern - search codebase for similar issues
2. **Low Risk**: Version mismatch on delete (optimistic locking not used for delete, which is correct)
