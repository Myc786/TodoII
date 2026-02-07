# Quickstart Guide: Todo App Feature Expansion

**Feature**: Todo App Feature Expansion
**Date**: 2026-02-02

## Overview
This guide provides step-by-step instructions for implementing the intermediate and advanced features for the Todo app, including priorities, tags, search, filters, sorting, due dates, reminders, and recurring tasks.

## Prerequisites
- Python 3.11+ with pip
- Node.js 18+ with npm
- Git
- SQLite 3.24+

## Phase 1: Intermediate Features Setup

### Step 1: Database Schema Updates

1. **Update the Task model** in `backend/src/models/task.py`:
   - Add priority field with enum values
   - Add due_date field
   - Add recurrence_pattern field
   - Add original_task_id field

2. **Create Tag model** in `backend/src/models/tag.py`:
   ```python
   from sqlmodel import SQLModel, Field
   from typing import Optional
   import uuid
   from datetime import datetime

   class Tag(SQLModel, table=True):
       id: Optional[uuid.UUID] = Field(default=None, primary_key=True)
       name: str = Field(nullable=False, min_length=1, max_length=50)
       color: Optional[str] = Field(default=None)  # Optional hex color
       user_id: uuid.UUID = Field(foreign_key="user.id", index=True)
       created_at: Optional[datetime] = Field(default=None)

       def __init__(self, **data):
           super().__init__(**data)
           if self.id is None:
               self.id = uuid.uuid4()
           if self.created_at is None:
               self.created_at = datetime.utcnow()
   ```

3. **Create TaskTag association model**:
   ```python
   from sqlmodel import SQLModel, Field
   import uuid

   class TaskTag(SQLModel, table=True):
       task_id: uuid.UUID = Field(foreign_key="task.id", primary_key=True)
       tag_id: uuid.UUID = Field(foreign_key="tag.id", primary_key=True)
   ```

4. **Update task schemas** in `backend/src/models/task_schemas.py`:
   - Add priority field to TaskCreate and TaskUpdate
   - Add tag_ids field to support tag assignment

5. **Create database migration** using Alembic or direct SQL:
   ```sql
   ALTER TABLE task ADD COLUMN priority VARCHAR(10) DEFAULT 'medium';
   ALTER TABLE task ADD COLUMN due_date TIMESTAMP NULL;
   ALTER TABLE task ADD COLUMN recurrence_pattern JSON NULL;
   ALTER TABLE task ADD COLUMN original_task_id UUID NULL REFERENCES task(id);

   CREATE TABLE tag (
       id UUID PRIMARY KEY,
       name VARCHAR(50) NOT NULL,
       color VARCHAR(7) NULL,
       user_id UUID NOT NULL REFERENCES user(id),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   CREATE TABLE task_tag (
       task_id UUID NOT NULL REFERENCES task(id) ON DELETE CASCADE,
       tag_id UUID NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
       PRIMARY KEY (task_id, tag_id)
   );
   ```

### Step 2: Backend Implementation

1. **Update TaskService** in `backend/src/services/task_service.py`:
   - Add methods for tag management
   - Update create_task to handle tags
   - Add search functionality
   - Add filtering and sorting capabilities

2. **Update Task API routes** in `backend/src/api/routes/tasks.py`:
   - Add search endpoint
   - Add filtering parameters to GET /tasks
   - Add tag management endpoints
   - Update existing endpoints to support new fields

3. **Create Tag API routes** in `backend/src/api/routes/tags.py`:
   - CRUD operations for tags
   - Assignment of tags to tasks

### Step 3: Frontend Implementation

1. **Update Task interface** in `frontend/src/lib/types.ts`:
   - Add priority field
   - Add due_date field
   - Add tags array
   - Add recurrence_pattern field

2. **Create Tag interface**:
   ```typescript
   export interface Tag {
     id: string;
     name: string;
     color?: string;
     user_id: string;
     created_at: string;
   }
   ```

3. **Update TaskCard component** in `frontend/src/components/task/task-card.tsx`:
   - Add priority indicator
   - Add due date display
   - Add tags display
   - Add visual indicators for overdue tasks

4. **Create TagInput component**:
   - Component for selecting and creating tags
   - Auto-complete functionality

5. **Update TaskForm component** in `frontend/src/components/task/task-form.tsx`:
   - Add priority selection dropdown
   - Add due date picker
   - Add tag input field
   - Add recurrence pattern selection

6. **Update TaskFilters component** in `frontend/src/components/task/task-filters.tsx`:
   - Add priority filter
   - Add tag filter
   - Add due date filter
   - Combine with existing status filter

7. **Create Search component**:
   - Real-time search input
   - Integration with task list

### Step 4: Testing

1. **Unit tests**: Write tests for new backend functionality
2. **Integration tests**: Test API endpoints with new features
3. **Component tests**: Test new frontend components

## Phase 2: Advanced Features Setup

### Step 1: Due Dates & Reminders

1. **Enhance Task model** with reminder functionality
2. **Create Reminder service** for scheduling notifications
3. **Implement browser notifications** in frontend
4. **Add reminder settings UI**

### Step 2: Recurring Tasks

1. **Create RecurringTaskTemplate model**
2. **Implement recurrence logic** in TaskService
3. **Add recurrence UI** to TaskForm
4. **Create background job** for generating recurring tasks

## Running the Application

1. **Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m src.main
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Verification Steps

1. **Create a task with priority and tags**
2. **Search for tasks using keywords**
3. **Apply filters and verify results**
4. **Sort tasks by different criteria**
5. **Set due dates and verify display**
6. **Create recurring tasks and verify generation**

## Troubleshooting

### Common Issues
- Database migration errors: Ensure all foreign key constraints are properly handled
- Frontend build errors: Check that all new interfaces are properly defined
- API validation errors: Verify that all new fields are properly validated

### Performance Considerations
- Large task lists: Implement proper pagination
- Search performance: Ensure proper indexing on search fields
- Filter performance: Index filtered columns appropriately