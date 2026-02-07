---
id: 0002
title: Create Implementation Plan for Task CRUD Fix
stage: plan
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-fix-task-crud
branch: 001-fix-task-crud
user: system
command: /sp.plan
labels: ["plan", "crud", "fix", "delete", "frontend"]
links:
  spec: specs/001-fix-task-crud/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-fix-task-crud/plan.md
  - specs/001-fix-task-crud/research.md
  - specs/001-fix-task-crud/data-model.md
  - specs/001-fix-task-crud/quickstart.md
  - specs/001-fix-task-crud/contracts/task-crud-api.yaml
tests:
  - N/A (planning phase)
---

## Prompt

Execute fixes for task update, completion toggle, and deletion,
then redeploy frontend and backend

--------------------------------------------------
PHASE 1 — DIAGNOSIS
--------------------------------------------------
1. Reproduce errors for:
   - Edit task
   - Mark complete/incomplete
   - Delete task
2. Capture failed requests in browser Network tab
3. Note HTTP methods, URLs, status codes

--------------------------------------------------
PHASE 2 — BACKEND FIXES
--------------------------------------------------
4. Verify endpoints exist:
   - PUT or PATCH /tasks/{id}
   - DELETE /tasks/{id}
5. Ensure task ID is correctly parsed
6. Update task fields (title, completed, etc.)
7. Return proper responses (200 or 204)

--------------------------------------------------
PHASE 3 — CORS & METHODS
--------------------------------------------------
8. Allow methods in CORS:
   - GET, POST, PUT, PATCH, DELETE, OPTIONS
9. Redeploy backend on Hugging Face Spaces

--------------------------------------------------
PHASE 4 — FRONTEND FIXES
--------------------------------------------------
10. Use correct HTTP methods and URLs
11. Send only required payload fields
12. Refresh task state after update/delete
13. Handle errors explicitly

--------------------------------------------------
PHASE 5 — DEPLOYMENT
--------------------------------------------------
14. Redeploy frontend on Vercel
15. Confirm env variables unchanged

--------------------------------------------------
PHASE 6 — VALIDATION
--------------------------------------------------
16. Test edit, complete toggle, and delete in production
17. Check no regressions in task creation

--------------------------------------------------
FINAL OUTPUT
--------------------------------------------------
- Edit, complete, delete actions work correctly
- UI updates instantly
- Stable production deployment

## Response snapshot

**Root Cause Identified**: The `handleTaskDeleted` function in `frontend/src/app/dashboard/page.tsx` (lines 59-61) only updates local React state - it does NOT call `apiClient.deleteTask()`. This causes delete operations to appear successful but not persist to the backend.

**Key Findings**:
- Backend API: All endpoints (PUT, DELETE, PATCH/toggle) correctly implemented ✓
- Frontend API client: All methods correctly implemented ✓
- CORS: Correctly configured with `allow_methods=["*"]` ✓
- Dashboard handlers: Update and Toggle work ✓, Delete is BROKEN ✗

**Plan Created**:
- Single-file fix in `frontend/src/app/dashboard/page.tsx`
- Change `handleTaskDeleted` to call `apiClient.deleteTask()` before state update
- 3 implementation phases: Fix, Verify, Deploy
- 5 test cases for verification

**Artifacts Generated**:
- `plan.md` - Full implementation plan
- `research.md` - Investigation findings
- `data-model.md` - Data model analysis (no changes needed)
- `quickstart.md` - Implementation guide
- `contracts/task-crud-api.yaml` - API contracts

## Outcome

- ✅ Impact: Root cause identified, implementation plan ready
- 🧪 Tests: 5 verification test cases defined
- 📁 Files: 5 planning artifacts created
- 🔁 Next prompts: `/sp.tasks` to generate task breakdown, then implement
- 🧠 Reflection: Single function bug - minimal fix required. Backend and API client were already correct.

## Evaluation notes (flywheel)

- Failure modes observed: None - clear root cause identified
- Graders run and results (PASS/FAIL): Constitution Check PASS, Technical Context complete
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
