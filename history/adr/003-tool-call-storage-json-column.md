# ADR-003: Store Tool Calls as JSON String vs Separate Table

> **Scope**: This ADR documents the decision to store MCP tool call information as a JSON string column in the messages table rather than creating a separate tool_calls table with normalized rows.

- **Status:** Accepted
- **Date:** 2026-02-06
- **Feature:** Todo AI Chatbot - Natural Language Todo Management (001-ai-chatbot)
- **Context:** Need to track which MCP tools were executed during conversation for debugging, audit trails, and potential UI display of tool usage

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: YES - Long-term consequence for data model, query patterns, and debugging capabilities
     2) Alternatives: YES - Multiple viable options (separate table vs. JSON column vs. no storage)
     3) Scope: YES - Cross-cutting concern affecting database schema, message persistence, and tool execution tracking
-->

## Decision

**Store tool call information as JSON string in `tool_calls` column of messages table**

Database schema:
```sql
CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversation(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    tool_calls TEXT,  -- JSON string: [{"tool": "add_task", "arguments": {...}, "result": {...}}]
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);
```

Tool calls JSON structure:
```json
[
  {
    "tool": "add_task",
    "arguments": {
      "user_id": "42",
      "title": "Buy groceries"
    },
    "result": {
      "task_id": 99,
      "status": "created",
      "title": "Buy groceries"
    }
  },
  {
    "tool": "list_tasks",
    "arguments": {
      "user_id": "42",
      "status": "pending"
    },
    "result": [
      {"task_id": 99, "title": "Buy groceries", "status": "pending"}
    ]
  }
]
```

**Usage Pattern**:
- Tool calls stored only for assistant messages (role='assistant')
- User messages have `tool_calls = null`
- JSON serialized in Python with `json.dumps()`, deserialized with `json.loads()`
- Tool calls always retrieved together with parent message (no joins needed)

## Consequences

### Positive

- **Simpler Schema**: Single table for messages, no complex joins for conversation history retrieval
- **Atomic Retrieval**: Tool calls always loaded with parent message (natural grouping)
- **Flexible Structure**: JSON allows varying tool call formats without schema migrations (e.g., adding new fields)
- **Faster Queries**: No JOIN required to get conversation history with tool calls (single table scan)
- **Easy Debugging**: All information about assistant response in one row (content + tool calls together)
- **Lower Maintenance**: No separate table to manage, migrate, or keep synchronized
- **Sufficient for Requirements**: Current requirements only need tool calls for debugging and UI display (not for analytics queries)

### Negative

- **No Individual Tool Call Queries**: Cannot easily query "all add_task calls across all conversations"
- **JSON Parsing Overhead**: Must deserialize JSON to access individual tool call details (minimal cost in Python)
- **No Referential Integrity**: Cannot enforce foreign keys on tool call data (e.g., task_id in result)
- **Limited Indexing**: Cannot index individual tool call fields (e.g., cannot index by tool name efficiently)
- **Denormalization**: Tool call data duplicated if multiple messages reference same tool call (unlikely in our use case)
- **Size Considerations**: Very large tool call results stored inline (may increase row size, but PostgreSQL handles TOAST compression)

## Alternatives Considered

### Alternative A: Separate tool_calls Table (Normalized)
```sql
CREATE TABLE tool_call (
    id SERIAL PRIMARY KEY,
    message_id INTEGER NOT NULL REFERENCES message(id) ON DELETE CASCADE,
    tool_name VARCHAR(50) NOT NULL,
    arguments JSONB NOT NULL,
    result JSONB,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_tool_call_message ON tool_call(message_id);
CREATE INDEX idx_tool_call_tool_name ON tool_call(tool_name);
```

**Why Rejected**:
- **Increased Query Complexity**: Every conversation history load requires JOIN between messages and tool_calls
  ```sql
  -- Complex query required
  SELECT m.*, tc.tool_name, tc.arguments, tc.result
  FROM message m
  LEFT JOIN tool_call tc ON tc.message_id = m.id
  WHERE m.conversation_id = $1
  ORDER BY m.created_at, tc.id;
  ```
- **Performance Overhead**: Additional JOIN on every chat request (violates stateless design simplicity)
- **Over-Engineering**: Building for analytics queries we don't need yet (YAGNI principle)
- **Schema Complexity**: Two tables to migrate, maintain, and keep synchronized
- **No Clear Benefit**: Current requirements don't need individual tool call queries
- **Constitution Violation**: "Prefer simpler solutions" - separate table adds complexity without immediate value

### Alternative B: JSONB Column (PostgreSQL Native JSON)
```sql
tool_calls JSONB  -- Native PostgreSQL JSON type instead of TEXT
```

**Why Rejected (Minor Difference)**:
- **JSONB Benefits**: Better indexing support (GIN indexes), native JSON operators (->>, @>, etc.)
- **JSONB Drawbacks**: Slightly larger storage footprint, parsing overhead on write (binary format)
- **Decision Rationale**: TEXT is sufficient for our use case:
  - We don't need to query individual tool call fields in SQL
  - All tool call access happens in Python (deserialize once per message)
  - Simpler migration (TEXT to JSONB is easy if needed later)
  - TEXT is more portable across databases (future flexibility)
- **Future Migration**: If we need JSON querying later, TEXT → JSONB migration is straightforward

### Alternative C: No Tool Call Storage (Events Only)
**Strategy**: Store tool calls in separate events/logs table for debugging, not in messages table

**Why Rejected**:
- **UI Requirements**: Frontend may want to show "Task created" indicators in chat (requires tool call data with messages)
- **Debugging**: Viewing conversation history without tool calls makes debugging difficult (need context of what agent did)
- **Audit Trail**: Tool calls are integral part of conversation flow, should be stored with messages
- **User Experience**: Showing which tools were used enhances transparency ("I created task #5 for you")

## Rationale

The decision prioritizes **schema simplicity** and **query performance** over **analytics flexibility**:

1. **Tool Calls Always Retrieved with Messages**: When loading conversation history, we always need tool calls together with assistant responses. Separate table would require JOINs on every request.

2. **No Analytics Requirements Yet**: Current requirements only need tool calls for:
   - Debugging (viewing conversation history with tool execution)
   - UI display (showing "Task created" indicators)
   - Audit trail (what agent did)

   We do NOT need:
   - "How many times was add_task called across all users?"
   - "What are the most common tool call failures?"
   - "Aggregate statistics by tool type"

3. **YAGNI Principle**: Building for hypothetical analytics queries is premature optimization. If we need analytics later, we can:
   - Add separate analytics table populated from tool_calls JSON
   - Migrate to JSONB and add GIN indexes
   - Extract tool calls to data warehouse

4. **JSON is Flexible**: Adding new fields to tool call structure (e.g., execution_time, error_code) doesn't require schema migrations.

5. **Performance Matters**: Stateless design loads conversation history on every request. Minimizing JOINs is critical for < 1 second load time.

## Implementation Guidelines

### Storing Tool Calls (Python)
```python
import json
from backend.src.models.message import Message

# After agent executes tools
tool_calls = [
    {
        "tool": "add_task",
        "arguments": {"user_id": "42", "title": "Buy groceries"},
        "result": {"task_id": 99, "status": "created", "title": "Buy groceries"}
    }
]

# Serialize and store
message = Message(
    conversation_id=conversation_id,
    user_id=user_id,
    role="assistant",
    content="I've created a new task: 'Buy groceries'",
    tool_calls=json.dumps(tool_calls)  # Serialize to JSON string
)
session.add(message)
session.commit()
```

### Retrieving Tool Calls (Python)
```python
import json

# Load conversation history
messages = session.query(Message).filter_by(
    conversation_id=conversation_id
).order_by(Message.created_at).all()

# Deserialize tool calls for assistant messages
for msg in messages:
    if msg.tool_calls:
        tool_calls = json.loads(msg.tool_calls)  # Parse JSON string
        # Use tool_calls list for debugging/UI
```

### Frontend Display
```typescript
interface ToolCall {
  tool: string;
  arguments: Record<string, any>;
  result: any;
}

interface Message {
  role: 'user' | 'assistant';
  content: string;
  tool_calls?: ToolCall[];  // Optional, only on assistant messages
}

// Display tool indicators
{message.tool_calls?.map(call => (
  <ToolIndicator key={call.tool} name={call.tool} result={call.result} />
))}
```

## Query Performance

**Conversation History Load** (single query, no JOINs):
```sql
SELECT id, role, content, tool_calls, created_at
FROM message
WHERE conversation_id = $1 AND user_id = $2
ORDER BY created_at ASC;
```

**Expected Performance**:
- 10 messages: < 10ms
- 50 messages: < 50ms
- 100 messages: < 100ms

**No JOIN overhead**, single table scan with index (`idx_message_conversation`)

## Future Migration Path

**If we need tool call analytics later**:

1. **Option 1: Add Analytics Table**
   ```sql
   CREATE TABLE tool_call_analytics (
       id SERIAL PRIMARY KEY,
       tool_name VARCHAR(50),
       user_id INTEGER,
       conversation_id INTEGER,
       executed_at TIMESTAMP,
       arguments JSONB,
       result JSONB
   );
   ```
   Populate via background job parsing `tool_calls` JSON from messages table

2. **Option 2: Migrate to JSONB**
   ```sql
   ALTER TABLE message ALTER COLUMN tool_calls TYPE JSONB USING tool_calls::jsonb;
   CREATE INDEX idx_tool_calls_gin ON message USING GIN (tool_calls);
   ```
   Enables JSON queries: `WHERE tool_calls @> '[{"tool": "add_task"}]'`

3. **Option 3: Extract to Data Warehouse**
   - ETL job exports tool_calls to analytics database (Snowflake, BigQuery, etc.)
   - Production database stays simple, analytics happens in warehouse

All three options are feasible without breaking existing code (JSON structure is preserved).

## References

- Feature Spec: `specs/1-ai-chatbot/spec.md` (Key Entities: Tool Call)
- Implementation Plan: `specs/001-ai-chatbot/plan.md` (Data Model Design)
- Related ADRs: ADR-001 (Cohere Integration), ADR-002 (Stateless Server Design)
- Database Schema: `specs/001-ai-chatbot/contracts/database-schema.sql`
- Constitution: `.specify/memory/constitution.md` (simplicity principles, YAGNI)

## Implementation Checkpoints

**Phase 2 (Foundational)**:
- [ ] Create message table with tool_calls TEXT column (task T008)
- [ ] Test JSON serialization/deserialization in Message model (task T010)

**Phase 3 (User Story 1)**:
- [ ] Store tool calls after agent execution (task T031)
- [ ] Return tool_calls in chat API response (task T034)
- [ ] Verify tool calls persist correctly (manual test)

**Phase 9 (Polish)**:
- [ ] Add tool call display in frontend MessageList component (task T088)
- [ ] Document tool_calls JSON format in API contracts (task T095)

## Success Criteria

- ✅ Tool calls stored successfully for all assistant messages with tool execution
- ✅ Conversation history load remains < 1 second with tool calls included
- ✅ Frontend can display tool execution indicators using tool_calls data
- ✅ Debugging conversations includes tool call information for troubleshooting
- ✅ No JOINs required for conversation history queries (single table scan)
