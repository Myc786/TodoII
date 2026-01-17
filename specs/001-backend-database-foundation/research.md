# Research: Backend & Database Foundation

## Decision: Authentication Strategy
**Rationale**: Using Better Auth on frontend with JWT plugin and manual JWT verification in FastAPI backend. This approach allows sharing the same BETTER_AUTH_SECRET between frontend and backend for token verification.
**Alternatives considered**:
- Full JWKS synchronization (more complex but more secure for production)
- Session-based authentication (contradicts the project requirement for JWT)
- Custom authentication solution (violates security-first principle)

## Decision: Database ORM Choice
**Rationale**: SQLModel selected as it provides unified schema for both database models and Pydantic validation as required by the project specifications.
**Alternatives considered**:
- SQLAlchemy + Pydantic (requires mapping between models)
- Tortoise ORM (async-only, doesn't fit well with FastAPI sync parts)
- Peewee (less feature-rich than SQLModel)

## Decision: State Management for Frontend
**Rationale**: React Server Components (RSC) for most views with Client Components for the Todo List to ensure real-time toggle responsiveness as specified in requirements.
**Alternatives considered**:
- Fully Client-Side Components (increased bundle size)
- SWR/React Query for data fetching (adds complexity without significant benefits)

## Decision: Concurrency Handling
**Rationale**: Optimistic locking with version numbers implemented at the database level to handle concurrent task modifications.
**Alternatives considered**:
- Pessimistic locking (would block users during edit)
- Last-write-wins (would potentially lose updates)
- Automatic merge (complex to implement correctly)

## Decision: API Communication Pattern
**Rationale**: JSON/REST communication between Next.js frontend and FastAPI backend with shared JWT secret for authentication.
**Alternatives considered**:
- GraphQL (adds complexity for simple CRUD operations)
- gRPC (overkill for web application)
- WebSocket for real-time updates (not required by basic specifications)

## Decision: Development Approach
**Rationale**: Following spec-driven task execution (read spec → generate plan → implement → test) as required by project constitution.
**Alternatives considered**:
- Agile iterative development (doesn't follow spec-driven approach)
- Test-driven development alone (doesn't emphasize spec-following)