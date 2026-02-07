# Quickstart: Fix Task CRUD Operations

**Feature**: 001-fix-task-crud
**Date**: 2026-02-07

## Problem Summary

Task delete operations fail to persist to the backend. The UI shows the task as deleted, but it reappears on page refresh.

## Root Cause

In `frontend/src/app/dashboard/page.tsx`, the `handleTaskDeleted` function (lines 59-61) only updates local React state without calling the backend API.

## The Fix

**File**: `frontend/src/app/dashboard/page.tsx`

### Before (Broken)

```typescript
// Lines 59-61
const handleTaskDeleted = (deletedTaskId: string) => {
  setTasks(prev => prev.filter(task => task.id !== deletedTaskId));
};
```

### After (Fixed)

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

Also update line 199 to use the new handler:
```typescript
onDelete={handleTaskDelete}
```

## Verification Steps

1. **Start local development**:
   ```bash
   # Terminal 1 - Backend
   cd backend
   uvicorn src.main:app --reload

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

2. **Test delete operation**:
   - Create a new task
   - Click the delete button
   - Refresh the page
   - Task should NOT reappear

3. **Test update operation** (should already work):
   - Edit a task's title
   - Refresh the page
   - Changes should persist

4. **Test toggle operation** (should already work):
   - Toggle task completion
   - Refresh the page
   - Status should persist

## Deployment

After fixing and testing locally:

1. **Deploy backend** (if any changes made):
   ```bash
   cd backend
   # Deploy to Hugging Face Spaces
   ```

2. **Deploy frontend**:
   ```bash
   cd frontend
   # Vercel auto-deploys on push to main
   git add .
   git commit -m "fix: task delete now calls backend API"
   git push origin main
   ```

## Files Changed

| File | Change |
|------|--------|
| `frontend/src/app/dashboard/page.tsx` | Fix delete handler to call API |
