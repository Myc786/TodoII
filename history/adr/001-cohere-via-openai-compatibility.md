# ADR-001: Use Cohere via OpenAI Compatibility Instead of Direct Cohere SDK

> **Scope**: This ADR documents the decision to use Cohere models through OpenAI's compatibility API rather than Cohere's native SDK, along with the choice of OpenAI Agents SDK as the agent runtime framework.

- **Status:** Accepted
- **Date:** 2026-02-06
- **Feature:** Todo AI Chatbot - Natural Language Todo Management (001-ai-chatbot)
- **Context:** Need an agent framework with tool calling capabilities to enable natural language task management through MCP tools

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: YES - Long-term consequence for AI integration architecture, affects all LLM interactions
     2) Alternatives: YES - Multiple viable options (direct Cohere SDK, LangChain, OpenAI Agents SDK)
     3) Scope: YES - Cross-cutting concern affecting agent runtime, tool integration, and future AI features
-->

## Decision

**Use OpenAI Agents SDK configured with Cohere models via OpenAI Compatibility API**

Technical implementation:
- **Agent Framework**: OpenAI Agents SDK (Python) - Agent + Runner classes
- **LLM Provider**: Cohere command-r-plus or command-a-03-2025 models
- **Integration Method**: OpenAI SDK with custom `base_url` pointing to Cohere's OpenAI-compatible endpoint
- **API Endpoint**: `https://api.cohere.ai/compatibility/v1`
- **Authentication**: Cohere API key passed to OpenAI client
- **Tool Integration**: MCP tools exposed to agent via OpenAI function calling format

Configuration example:
```python
from openai import OpenAI

client = OpenAI(
    base_url="https://api.cohere.ai/compatibility/v1",
    api_key=os.getenv("COHERE_API_KEY")
)

# Agent uses client with Cohere model
agent = Agent(
    client=client,
    model="command-r-plus",
    instructions="You are a helpful task management assistant...",
    tools=mcp_tools
)
```

## Consequences

### Positive

- **Mature Agent Runtime**: OpenAI Agents SDK provides production-ready agent orchestration with tool calling, message history management, and error handling
- **Standard Interface**: OpenAI-compatible API is an industry standard, making future LLM provider switches easier (e.g., could switch to Anthropic, OpenAI, or other compatible providers)
- **Best-in-Class Tool Integration**: OpenAI function calling format is well-documented and widely supported by MCP SDK and other tool frameworks
- **Simplified Development**: Single SDK handles both LLM communication and agent workflow (no custom agent loop implementation needed)
- **Future-Proof**: Compatibility API insulates us from Cohere SDK breaking changes while maintaining access to latest models
- **Reduced Dependencies**: No need for separate Cohere SDK + custom agent framework (e.g., LangChain)

### Negative

- **API Indirection Layer**: Adds one hop between application and Cohere's native API (Cohere compatibility endpoint → Cohere native API)
- **Potential Feature Lag**: Cohere-specific features may not be immediately available through compatibility API
- **Limited Cohere Optimization**: Cannot use Cohere-native optimizations or parameters not supported by OpenAI format
- **Dual API Key Management**: Need to manage Cohere API key even though using OpenAI SDK (minor operational complexity)
- **Compatibility API Reliability**: Dependent on Cohere maintaining compatibility endpoint with feature parity

## Alternatives Considered

### Alternative A: Direct Cohere SDK + Custom Agent Loop
- **Components**: Native Cohere SDK, custom agent orchestration code
- **Why Rejected**:
  - Requires building custom agent loop (message history, tool calling workflow, error handling, retry logic)
  - Higher development and maintenance cost
  - Cohere SDK lacks mature agent runtime (focused on chat completions)
  - Would need to implement tool calling orchestration from scratch
  - Reinventing wheel when production-ready solutions exist

### Alternative B: LangChain + Direct Cohere SDK
- **Components**: LangChain framework, Cohere LangChain integration
- **Why Rejected**:
  - LangChain is heavyweight with steep learning curve
  - Adds significant dependency overhead (dozens of packages)
  - Over-engineered for our needs (we don't need chains, retrieval, multiple agents)
  - LangChain Cohere integration may lag behind Cohere SDK updates
  - Constitution principle: prefer simpler solutions when they meet requirements

### Alternative C: OpenAI Native Models
- **Components**: OpenAI SDK with GPT-4 or GPT-3.5-turbo
- **Why Rejected**:
  - Higher cost per token compared to Cohere command models
  - Constitution specifies Cohere for cost optimization
  - OpenAI rate limits more restrictive for new accounts
  - Would lock us into OpenAI pricing and terms
  - Cohere command-r-plus provides comparable quality at lower cost

### Alternative D: Anthropic Claude + Custom Agent
- **Components**: Anthropic SDK, custom agent orchestration
- **Why Rejected**:
  - Same custom agent loop problems as Alternative A
  - Higher cost than Cohere
  - Anthropic SDK lacks agent runtime (chat completions only)
  - Would need custom tool calling implementation

## Rationale

The decision prioritizes **developer velocity** and **production readiness** over native API optimization:

1. **Agent Runtime is Non-Negotiable**: Building a reliable agent orchestration system is complex (message history, tool execution, error handling, retries). OpenAI Agents SDK solves this out-of-the-box.

2. **Cohere Cost Benefits Preserved**: Using Cohere via compatibility API maintains cost advantages over OpenAI/Anthropic while gaining mature agent runtime.

3. **Standard Interface Wins**: OpenAI-compatible API is the de facto standard for LLM integrations. This decision aligns with industry direction and maximizes compatibility.

4. **Indirection Cost is Minimal**: The extra API hop adds negligible latency (<50ms) compared to model inference time (1-3 seconds). This is an acceptable trade-off for development velocity.

5. **MCP Integration**: MCP SDK provides tool schemas in OpenAI function calling format, making integration seamless with OpenAI Agents SDK.

## References

- Feature Spec: `specs/1-ai-chatbot/spec.md`
- Implementation Plan: `specs/001-ai-chatbot/plan.md`
- Research Document: `specs/001-ai-chatbot/research.md` (Cohere compatibility API validation)
- Related ADRs: ADR-002 (Stateless Server Design), ADR-003 (Tool Call Storage)
- Constitution: `.specify/memory/constitution.md` (cost optimization principles, prefer Cohere)
- Cohere Compatibility API Docs: https://docs.cohere.com/docs/openai-compatibility
- OpenAI Agents SDK: https://github.com/openai/openai-python (agents module)
- MCP SDK Documentation: https://modelcontextprotocol.io/

## Implementation Notes

**Environment Variables Required**:
```bash
COHERE_API_KEY=<cohere-api-key>
OPENAI_COMPAT_BASE_URL=https://api.cohere.ai/compatibility/v1
COHERE_MODEL_NAME=command-r-plus
```

**Testing Strategy**:
- Phase 0: Validate Cohere compatibility API supports function calling with MCP tools
- Phase 2: Proof-of-concept with simple agent + single MCP tool
- Phase 3: Integration tests with all 5 MCP tools + conversation history

**Rollback Plan**:
If Cohere compatibility API proves insufficient:
1. **Fallback Option 1**: Switch to LangChain + Direct Cohere SDK (1-2 day rework)
2. **Fallback Option 2**: Switch to OpenAI GPT-4 models (configuration change only, higher cost)

**Future Considerations**:
- Monitor Cohere compatibility API feature parity with native API
- Evaluate streaming response support for better UX in future iterations
- Consider Cohere-native SDK if compatibility API becomes limiting factor
