# Research Document: Todo App Feature Expansion

**Feature**: Todo App Feature Expansion
**Date**: 2026-02-02

## Database Schema Extensions

### Decision: Task Model Extension
**Rationale**: Extending the existing Task model is the most straightforward approach that maintains compatibility with existing code while adding the required functionality.

**Implementation Approach**:
- Add `priority` field as enum with values: 'high', 'medium', 'low'
- Add `due_date` field as datetime (nullable)
- Add `recurrence_pattern` field as string (nullable) for storing recurrence rules
- Create separate `Tag` model with many-to-many relationship to Task
- Create `TaskTag` association table

### Decision: Tag System Implementation
**Rationale**: Using a normalized many-to-many relationship between Task and Tag models provides flexibility and follows database best practices.

**Alternatives Considered**:
1. JSON field in Task model
   - Pros: Simple implementation, no additional tables
   - Cons: Difficult to query, no referential integrity, inefficient for filtering
2. Comma-separated string in Task model
   - Pros: Very simple
   - Cons: Impossible to query efficiently, violates normalization principles
3. Normalized many-to-many relationship (chosen)
   - Pros: Efficient querying, referential integrity, scalable
   - Cons: Additional complexity with join table

### Decision: Search Implementation
**Rationale**: SQLite's built-in full-text search (FTS5) module provides efficient text search capabilities without requiring external dependencies.

**Implementation Approach**:
- Use SQLite FTS5 virtual tables for efficient searching
- Create triggers to keep FTS table synchronized with main task table
- Search across title and description fields

## Recurrence System Design

### Decision: Recurrence Pattern Storage
**Rationale**: Storing recurrence patterns as structured data allows for flexible rule definitions while maintaining readability.

**Pattern Format**:
- Daily: `{"type": "daily", "interval": 1}`
- Weekly: `{"type": "weekly", "days": ["monday", "wednesday", "friday"]}`
- Monthly: `{"type": "monthly", "day_of_month": 15}`
- Custom: `{"type": "custom", "interval_days": 7}`

### Decision: Task Instance Generation
**Rationale**: Generating new task instances when previous ones are completed ensures that recurring tasks continue without requiring background jobs to constantly monitor and create tasks.

**Implementation Approach**:
- When a recurring task is marked as complete, generate the next instance based on the recurrence pattern
- Store the original task template separately to preserve recurrence rules
- Link instances to their template for historical tracking

## Notification System

### Decision: Two-Tier Notification System
**Rationale**: Combining browser notifications with backend scheduling provides reliable delivery while maintaining user experience.

**Implementation Approach**:
1. Frontend: Browser notifications for immediate alerts
2. Backend: Background job scheduler to check for upcoming due tasks
3. Fallback: Email notifications for missed browser notifications (future enhancement)

## Performance Considerations

### Decision: Database Indexing Strategy
**Rationale**: Proper indexing is crucial for maintaining performance as the number of tasks grows.

**Indexing Plan**:
- Index on `user_id` (already exists)
- Index on `completed` status for filtering
- Index on `priority` for priority-based queries
- Index on `due_date` for due date filtering
- Composite indexes for combined filters

### Decision: Pagination Strategy
**Rationale**: Implementing pagination prevents performance issues when users have large numbers of tasks.

**Implementation**:
- Default page size: 50 tasks
- Cursor-based pagination for better performance
- Infinite scroll implementation in frontend

## Security Considerations

### Decision: Input Validation Strategy
**Rationale**: Proper validation prevents injection attacks and ensures data integrity.

**Validation Approach**:
- Server-side validation for all API endpoints
- Sanitization of user inputs
- Validation of recurrence patterns to prevent malicious code
- Rate limiting for API endpoints