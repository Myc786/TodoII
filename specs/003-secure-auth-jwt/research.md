# Research: Secure Auth & JWT Integration

## Decision: Token Verification
**Rationale**: Using the jose library in Python to decode and verify JWTs. The python-jose library provides robust JWT handling capabilities with support for various signing algorithms.
**Alternatives considered**:
- PyJWT (also a solid option but jose has broader algorithm support)
- Custom implementation (not recommended for security reasons)

## Decision: Signing Algorithm
**Rationale**: Using a shared secret (BETTER_AUTH_SECRET) for HS256 signing/verification to keep the integration simple and fast for the hackathon. HS256 provides a good balance of security and simplicity.
**Alternatives considered**:
- RS256 with public/private key pairs (more complex setup but allows for distributed verification)
- Asymmetric cryptography (adds complexity without significant benefit for this use case)

## Decision: Authentication Context Injection
**Rationale**: Using FastAPI's Depends() to inject the current_user directly into route functions. This ensures that any route needing a user ID has it automatically verified before the logic executes.
**Alternatives considered**:
- Manual token verification in each endpoint (repetitive and error-prone)
- Global middleware (less granular control over which endpoints are protected)

## Decision: Middleware vs. Dependencies
**Rationale**: Using a Dependency-based approach for routes to have granular control over which endpoints are public vs. private. This allows for flexible endpoint protection while maintaining clean separation of concerns.
**Alternatives considered**:
- Global authentication middleware (would protect all endpoints uniformly)
- Decorator-based approach (possible but less integrated with FastAPI's dependency system)

## Decision: Frontend Authentication State Management
**Rationale**: Implementing a custom authentication hook (useAuth) to manage the authentication state on the frontend, integrating with Better Auth for session management and JWT handling.
**Alternatives considered**:
- Storing JWT in local storage (vulnerable to XSS attacks)
- Using HTTP-only cookies (more secure but adds complexity with CSRF protection)

## Decision: API Client JWT Attachment
**Rationale**: Updating the existing API client to automatically attach JWT tokens to the Authorization: Bearer header for all authenticated requests. This centralizes the authentication logic.
**Alternatives considered**:
- Manually adding headers to each request (error-prone and repetitive)
- Separate authenticated API client instance (adds complexity without significant benefit)