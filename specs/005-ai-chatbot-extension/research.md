# Research Findings: AI-Powered Todo Chatbot Extension

**Feature**: AI-Powered Todo Chatbot Extension
**Date**: 2026-01-17

## Research Task 0.1: MCP SDK Integration Patterns

### Decision: Use Official MCP SDK with Next.js App Router
**Rationale**: The MCP SDK provides standardized interfaces for connecting AI agents to backend services. For Next.js 16+ App Router, we'll implement the MCP tools as server-side functions that can be called from the chatbot agent.

**Implementation Approach**:
- Create MCP tool definitions in a dedicated directory
- Use server actions for MCP tools that interact with backend APIs
- Implement proper authentication context passing
- Follow existing backend service patterns for consistency

**Alternatives Considered**:
- Direct API calls from client: Would bypass security requirements
- Custom RPC mechanism: Would reinvent existing standards

## Research Task 0.2: OpenAI ChatKit UI Integration

### Decision: Integrate ChatKit with Floating Widget Pattern
**Rationale**: The OpenAI ChatKit provides pre-built UI components that can be customized to fit the existing theme system. The floating widget approach minimizes UI disruption while providing easy access.

**Implementation Approach**:
- Use ChatKit's React components for message handling
- Create a floating container component that integrates with existing layout
- Implement theme context passing to ensure consistent styling
- Add smooth animations for expand/collapse functionality

**Alternatives Considered**:
- Building from scratch: Higher development time, less reliability
- Third-party chat widgets: Less control over integration

## Research Task 0.3: Authentication Context Management

### Decision: Propagate JWT Token Through Chat Session Context
**Rationale**: The existing JWT authentication system should be leveraged to maintain security. The token will be passed from the frontend through the chatbot to MCP tools.

**Implementation Approach**:
- Extract JWT from browser session in frontend
- Pass token securely to chatbot agent context
- Validate token in each MCP tool before executing operations
- Implement token refresh mechanisms if needed

**Alternatives Considered**:
- Separate authentication for chatbot: Would create security gaps
- Session-based auth: Would duplicate existing JWT infrastructure

## Research Task 0.4: Natural Language Understanding Patterns

### Decision: Combine OpenAI GPT with Structured Intent Recognition
**Rationale**: While OpenAI's models are excellent at understanding natural language, combining them with structured intent recognition improves reliability for task-specific operations.

**Implementation Approach**:
- Use system prompt to define todo management domain
- Implement structured output parsing for command validation
- Add fallback mechanisms for ambiguous commands
- Include examples in system prompt for better accuracy

**Alternatives Considered**:
- Rule-based parsing: Less flexible for natural language variations
- Pure ML classification: Requires training data and maintenance