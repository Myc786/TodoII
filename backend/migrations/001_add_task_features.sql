-- Migration: Add priority, due_date, recurrence_pattern, and original_task_id fields to task table
-- This migration adds the new columns required for the Todo App feature expansion

-- Add columns to existing task table
ALTER TABLE task ADD COLUMN priority VARCHAR(10) DEFAULT 'medium';
ALTER TABLE task ADD COLUMN due_date TIMESTAMP NULL;
ALTER TABLE task ADD COLUMN recurrence_pattern JSON NULL;
ALTER TABLE task ADD COLUMN original_task_id UUID NULL;

-- Add foreign key constraint for original_task_id
ALTER TABLE task ADD CONSTRAINT fk_task_original_task
    FOREIGN KEY (original_task_id) REFERENCES task(id) ON DELETE SET NULL;

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_task_priority ON task(priority);
CREATE INDEX IF NOT EXISTS idx_task_due_date ON task(due_date);
CREATE INDEX IF NOT EXISTS idx_task_completed ON task(completed);

-- Create tag table
CREATE TABLE IF NOT EXISTS tag (
    id UUID PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    color VARCHAR(7) NULL,
    user_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Create indexes for tag table
CREATE INDEX IF NOT EXISTS idx_tag_user_id ON tag(user_id);
CREATE INDEX IF NOT EXISTS idx_tag_name ON tag(name);

-- Create task_tag association table
CREATE TABLE IF NOT EXISTS task_tag (
    task_id UUID NOT NULL,
    tag_id UUID NOT NULL,
    PRIMARY KEY (task_id, tag_id),
    FOREIGN KEY (task_id) REFERENCES task(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tag(id) ON DELETE CASCADE
);

-- Create indexes for task_tag table
CREATE INDEX IF NOT EXISTS idx_task_tag_task_id ON task_tag(task_id);
CREATE INDEX IF NOT EXISTS idx_task_tag_tag_id ON task_tag(tag_id);