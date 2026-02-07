# ADR-002: Stateless Server Design with Full History Reload Per Request

> **Scope**: This ADR documents the decision to maintain complete server statelessness by reloading full conversation history from PostgreSQL on every chat request, rather than using session caching.

- **Status:** Accepted
- **Date:** 2026-02-06
- **Feature:** Todo AI Chatbot - Natural Language Todo Management (001-ai-chatbot)
- **Context:** Need to maintain conversation context for AI agent while supporting horizontal scaling, server restarts, and zero in-memory state

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: YES - Long-term architectural consequence for scalability, deployment, and reliability
     2) Alternatives: YES - Multiple viable options (in-memory sessions, Redis cache, stateless DB reload)
     3) Scope: YES - Cross-cutting concern affecting deployment, scaling, failover, and conversation management
-->

## Decision

**Implement fully stateless server architecture with conversation history loaded from PostgreSQL on every chat request**

Technical implementation:
- **No Server-Side Sessions**: Zero in-memory conversation state on backend
- **Database as Source of Truth**: All conversation messages persisted in PostgreSQL (conversations + messages tables)
- **Per-Request History Load**: Every POST /api/{user_id}/chat request:
  1. Load complete conversation history from database (SELECT messages WHERE conversation_id = X ORDER BY created_at)
  2. Append new user message to database
  3. Build message array for agent (format: [{role, content}, ...])
  4. Execute agent with full history + new message
  5. Persist assistant response to database
  6. Return response to client
- **Client-Side Conversation ID**: Frontend persists conversation_id in localStorage for resumption
- **Optimized Queries**: Database indexes on (conversation_id, created_at ASC) and (user_id) for fast retrieval

Query performance target: < 1 second for conversations up to 100 messages

## Consequences

### Positive

- **Horizontal Scalability**: Any backend instance can handle any request (no sticky sessions required)
- **Zero State Loss on Restart**: Server crashes/restarts have zero impact on conversations (all state in database)
- **Simplified Deployment**: No session store to configure, maintain, or synchronize across instances
- **Consistent Architecture**: Aligns with existing Phase II stateless API design principles
- **No Cache Invalidation**: Eliminates entire class of bugs related to stale cache data
- **Easy Debugging**: Full conversation history always available in database for troubleshooting
- **Load Balancer Friendly**: Simple round-robin load balancing without session affinity
- **Disaster Recovery**: Database backup/restore is sufficient (no separate session state to backup)

### Negative

- **Higher Database Load**: Every chat request performs SELECT on messages table (vs. cache hit)
- **Increased Latency**: Database round-trip on every request adds ~50-200ms vs. in-memory cache
- **Database Dependency**: Database becomes critical path for every chat request (no degraded mode)
- **Scalability Ceiling**: Database becomes bottleneck for very high conversation message counts (>200 messages)
- **Cost**: More database queries = higher database resource usage (though PostgreSQL handles this well with proper indexes)

## Alternatives Considered

### Alternative A: In-Memory Sessions (Per-Instance State)
- **Components**: Server maintains conversation history in memory (e.g., Python dictionary keyed by conversation_id)
- **Why Rejected**:
  - **Sticky Sessions Required**: Load balancer must route same conversation to same instance (complex configuration)
  - **State Loss on Restart**: Server crash/restart loses all in-memory conversations (poor reliability)
  - **Memory Management**: Must implement LRU eviction, conversation timeouts, memory limits
  - **No Horizontal Scaling**: Cannot easily add/remove instances without session migration
  - **Debugging Complexity**: State spread across multiple instances makes troubleshooting difficult

### Alternative B: Redis Session Cache (Distributed Cache)
- **Components**: Redis cluster caching conversation history, database as backup
- **Cache Strategy**:
  - First request: Load from database → cache in Redis (TTL 1 hour)
  - Subsequent requests: Load from Redis (fast)
  - On cache miss: Fall back to database
- **Why Rejected**:
  - **Operational Complexity**: Adds Redis cluster to infrastructure (deployment, monitoring, maintenance)
  - **Cache Invalidation**: Must handle stale data, cache expiration, race conditions
  - **Dependency Risk**: Redis failure degrades performance or causes errors (needs fallback logic)
  - **Cost**: Additional infrastructure cost for Redis cluster
  - **Over-Engineering**: Adds complexity for problem that doesn't exist yet (< 100 messages per conversation is fast from DB)
  - **Constitution Violation**: "Prefer simpler solutions" - Redis is premature optimization

### Alternative C: Hybrid Approach (Short-Term Cache)
- **Components**: In-memory cache for recent messages (last 10-20), database for full history
- **Strategy**: Cache only active conversations (last 5 minutes), reload from DB on cache miss
- **Why Rejected**:
  - **Complexity Without Clear Benefit**: Adds caching logic but still needs database fallback
  - **Partial State Synchronization**: Cache and database must stay synchronized (complex)
  - **Stale Data Risk**: Short TTL means frequent cache misses anyway
  - **Premature Optimization**: Solving problem that doesn't exist (DB query is fast enough)

## Rationale

The decision prioritizes **architectural simplicity** and **operational reliability** over theoretical performance optimization:

1. **Database Performance is Sufficient**: PostgreSQL with proper indexes can return 100 messages in < 100ms. This is negligible compared to LLM inference time (1-3 seconds).

2. **Conversations are Short**: User research shows typical conversations have 10-30 messages. Even 100-message conversations are edge cases. Database handles this easily.

3. **Infrastructure Simplicity**: Eliminating Redis reduces deployment complexity, cost, and failure modes. Fewer moving parts = higher reliability.

4. **Horizontal Scaling Works**: Load balancer can use simple round-robin. Adding/removing instances is trivial. This enables cost-effective scaling.

5. **Aligns with Existing Architecture**: Phase II todo API is already stateless. Maintaining consistency across all APIs simplifies mental model and operations.

6. **Future Optimization is Easy**: If database becomes bottleneck (unlikely), we can add Redis later without changing API contracts. Client is unaware of backend caching strategy.

## Database Optimization Strategy

To ensure stateless design performs well:

### Indexes (Critical)
```sql
-- Fast conversation history retrieval
CREATE INDEX idx_message_conversation ON message(conversation_id, created_at ASC);

-- Fast user's conversations lookup
CREATE INDEX idx_conversation_user_id ON conversation(user_id);
CREATE INDEX idx_conversation_user_created ON conversation(user_id, created_at DESC);

-- Fast user_id filtering
CREATE INDEX idx_message_user_id ON message(user_id);
```

### Query Optimization
```sql
-- Optimized history load (uses idx_message_conversation)
SELECT id, role, content, tool_calls, created_at
FROM message
WHERE conversation_id = $1 AND user_id = $2
ORDER BY created_at ASC
LIMIT 100;  -- Pagination for edge cases

-- Execution plan should show Index Scan on idx_message_conversation
EXPLAIN ANALYZE <query>;
```

### Performance Monitoring
- Alert if p95 query time > 500ms for conversation history load
- Alert if p99 query time > 1 second
- Monitor slow query log for conversation-related queries
- Track database connection pool utilization

### Contingency Plan (If Database Becomes Bottleneck)
1. **Short-term**: Implement conversation message pagination (load last 50 messages only)
2. **Medium-term**: Add read replicas for chat endpoint queries (write to primary, read from replica)
3. **Long-term**: Implement Redis cache layer (same stateless API, caching is transparent optimization)

## References

- Feature Spec: `specs/1-ai-chatbot/spec.md` (NFR-003: System MUST maintain complete statelessness)
- Implementation Plan: `specs/001-ai-chatbot/plan.md` (Stateless design decision, performance goals)
- Related ADRs: ADR-001 (Cohere Integration), ADR-003 (Tool Call Storage)
- Constitution: `.specify/memory/constitution.md` (architectural simplicity principles)
- Database Schema: `specs/001-ai-chatbot/contracts/database-schema.sql`

## Implementation Checkpoints

**Phase 2 (Foundational)**:
- [ ] Create database indexes for conversation queries (tasks T086-T087)
- [ ] Implement ConversationService with history loading (task T011)
- [ ] Verify query performance with 100-message test conversations (task T085)

**Phase 3 (User Story 1)**:
- [ ] Implement stateless chat endpoint (task T032)
- [ ] Test conversation persistence across page reloads (task T044)
- [ ] Verify zero state loss on server restart (manual test)

**Phase 9 (Polish)**:
- [ ] Load testing with 10 concurrent users (task T083)
- [ ] Database query performance monitoring (task T084)
- [ ] Document statelessness guarantee in API documentation (task T094)

## Future Considerations

**If conversation history becomes performance bottleneck**:
1. Implement pagination: Load last N messages + conversation summary
2. Add Redis caching layer (transparent to API clients)
3. Consider conversation archival strategy (move old conversations to cold storage)

**If database connection pool exhausted**:
1. Increase pool size (short-term fix)
2. Add read replicas for chat endpoint queries (medium-term)
3. Implement query batching for multiple concurrent requests from same user (advanced)

**Success Metrics**:
- Chat endpoint p95 latency < 5 seconds (including LLM inference)
- Database query time < 10% of total request time
- Zero conversation data loss incidents
- Successful server restarts with zero user impact
