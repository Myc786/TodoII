# Phase III: Todo AI Chatbot - Research

**Researched:** 2026-02-06
**Domain:** AI Chatbot Integration with MCP Tools
**Confidence:** MEDIUM

## Summary

Research has been conducted on four key technologies needed for implementing the Todo AI Chatbot feature:

1. **Cohere via OpenAI Compatibility API** - Cohere provides OpenAI-compatible endpoints, but specific documentation for the compatibility layer requires verification
2. **OpenAI Python SDK** - Well-documented SDK supporting custom base URLs for alternative LLM providers
3. **MCP (Model Context Protocol) Python SDK** - Provides multiple transport options (stdio, SSE, HTTP) with FastAPI/ASGI integration support
4. **Frontend Chat UI** - OpenAI ChatKit package existence needs verification; alternative React-based chat UI libraries available

**Primary recommendation:** Use MCP Python SDK with SSE or HTTP transport for FastAPI integration, OpenAI Python SDK with custom base_url for Cohere, and evaluate alternative chat UI libraries if OpenAI ChatKit is not available.

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| openai | 1.0+ | OpenAI Python SDK | Industry standard for OpenAI-compatible APIs, supports custom endpoints |
| mcp | latest | Model Context Protocol SDK | Official MCP implementation for Python servers |
| FastAPI | 0.100+ | Web framework | Already used in project backend |
| cohere | latest | Cohere SDK (optional) | Native Cohere integration if OpenAI compatibility has limitations |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| httpx | 0.24+ | Async HTTP client | For MCP tool implementations making external API calls |
| pydantic | 2.0+ | Data validation | Tool parameter validation in MCP |
| python-dotenv | 1.0+ | Environment management | Secure API key storage |

### Frontend Options
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| react-chatbot-kit | 2.0+ | React chat UI | If OpenAI ChatKit unavailable |
| @chatscope/chat-ui-kit-react | 1.10+ | React chat components | Alternative chat UI |
| Custom implementation | - | Tailored UI | Maximum control and integration |

**Installation (Backend):**
```bash
pip install openai mcp httpx pydantic python-dotenv
```

**Installation (Frontend - to be verified):**
```bash
npm install @openai/chatkit  # If available
# OR
npm install react-chatbot-kit @chatscope/chat-ui-kit-react
```

## Architecture Patterns

### Recommended Project Structure
```
backend/
├── src/
│   ├── api/
│   │   └── routes/
│   │       └── chat.py          # Chat completion endpoint
│   ├── services/
│   │   ├── chat_service.py      # LLM interaction logic
│   │   └── mcp_server.py        # MCP tool server
│   ├── mcp/
│   │   ├── tools/
│   │   │   ├── task_tools.py    # Task CRUD tools
│   │   │   ├── tag_tools.py     # Tag management tools
│   │   │   └── reminder_tools.py # Reminder tools
│   │   └── server.py            # MCP server setup
│   └── models/
│       └── chat_schemas.py      # Chat request/response models

frontend/
├── src/
│   ├── components/
│   │   └── chat/
│   │       ├── chat-interface.tsx    # Main chat UI
│   │       ├── chat-message.tsx      # Message component
│   │       └── chat-input.tsx        # Input component
│   ├── lib/
│   │   └── chat-api.ts               # Chat API client
│   └── app/
│       └── chat/
│           └── page.tsx              # Chat page
```

### Pattern 1: OpenAI SDK with Custom Endpoint (Cohere)
**What:** Configure OpenAI Python SDK to use Cohere's API endpoint
**When to use:** When using Cohere models with OpenAI-compatible interface

**Example:**
```python
# Source: OpenAI Python SDK GitHub README
from openai import OpenAI

# Configure client with Cohere endpoint
client = OpenAI(
    base_url="https://api.cohere.ai/v1",  # Cohere OpenAI-compatible endpoint
    api_key=os.getenv("COHERE_API_KEY")
)

# Use chat completions as normal
response = client.chat.completions.create(
    model="command-r-plus",  # Cohere model name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

**Note:** The exact Cohere OpenAI-compatible endpoint URL requires verification. Alternative paths may include:
- `https://api.cohere.ai/v1` (standard v1 endpoint)
- `https://api.cohere.ai/v1/chat` (direct chat endpoint)
- Cohere-specific compatibility endpoint (to be verified with Cohere docs)

### Pattern 2: MCP Server with FastAPI Integration
**What:** Mount MCP server to existing FastAPI application using SSE or HTTP transport
**When to use:** For exposing task management tools to the LLM

**Example:**
```python
# Source: MCP Python SDK GitHub and modelcontextprotocol.io
from mcp.server.mcpserver import MCPServer
from starlette.applications import Starlette
from starlette.routing import Mount
from fastapi import FastAPI

# Create MCP server
mcp = MCPServer("Todo MCP Server")

# Define tools
@mcp.tool()
async def create_task(
    title: str,
    description: str,
    priority: str = "medium"
) -> dict:
    """Create a new task in the todo list"""
    # Implementation calls task service
    return {"task_id": "123", "status": "created"}

@mcp.tool()
async def list_tasks(status: str = "all") -> list:
    """List all tasks, optionally filtered by status"""
    # Implementation calls task service
    return [{"id": "1", "title": "Task 1"}]

# Mount to FastAPI
app = FastAPI()

# Option 1: SSE transport (recommended for browser clients)
app.mount("/mcp", mcp.streamable_http_app())

# Option 2: Direct ASGI mounting (from Starlette example)
# starlette_app = Starlette(routes=[Mount("/mcp", app=mcp.streamable_http_app())])
```

### Pattern 3: Chat Service with MCP Tool Integration
**What:** Chat service that calls LLM and executes MCP tools based on LLM responses
**When to use:** Core chat logic that bridges LLM and tool execution

**Example (Conceptual - requires verification):**
```python
from openai import OpenAI
from typing import List, Dict

class ChatService:
    def __init__(self, mcp_client):
        self.llm = OpenAI(
            base_url="https://api.cohere.ai/v1",
            api_key=os.getenv("COHERE_API_KEY")
        )
        self.mcp_client = mcp_client

    async def chat(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """Process chat with tool execution"""
        # Call LLM with available tools
        response = self.llm.chat.completions.create(
            model="command-r-plus",
            messages=messages,
            tools=tools  # MCP tools formatted as OpenAI tools
        )

        # If LLM wants to use a tool
        if response.choices[0].message.tool_calls:
            tool_call = response.choices[0].message.tool_calls[0]

            # Execute MCP tool
            tool_result = await self.mcp_client.call_tool(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )

            # Return result to LLM for final response
            messages.append(response.choices[0].message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result)
            })

            # Get final response
            final_response = self.llm.chat.completions.create(
                model="command-r-plus",
                messages=messages
            )

            return final_response

        return response
```

### Pattern 4: Frontend Chat Integration
**What:** React component that connects to chat API endpoint
**When to use:** User-facing chat interface

**Example (Generic React Pattern):**
```typescript
// src/components/chat/chat-interface.tsx
import { useState } from 'react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: 'user' as const, content: input }];
    setMessages(newMessages);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages })
      });

      const data = await response.json();
      setMessages([...newMessages, { role: 'assistant' as const, content: data.content }]);
    } catch (error) {
      console.error('Chat error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message ${msg.role}`}>
            {msg.content}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          disabled={loading}
        />
        <button onClick={sendMessage} disabled={loading}>
          Send
        </button>
      </div>
    </div>
  );
}
```

### Anti-Patterns to Avoid
- **Stdio transport for web servers:** Stdio is for desktop apps (Claude Desktop), not web servers. Use SSE or HTTP transport for FastAPI.
- **Hardcoded API keys:** Always use environment variables for Cohere API keys
- **Logging to stdout in MCP servers:** Corrupts JSON-RPC messages; use stderr or file logging
- **Single monolithic chat endpoint:** Separate concerns - chat logic, tool execution, and state management should be modular

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Chat UI components | Custom chat bubbles, scrolling, input handling | react-chatbot-kit or @chatscope/chat-ui-kit-react | Handles message rendering, auto-scroll, typing indicators, accessibility |
| OpenAI-compatible client | Custom HTTP client for LLM APIs | OpenAI Python SDK with base_url | Handles retries, rate limiting, streaming, error handling |
| Tool schema generation | Manual JSON schema creation | MCP @mcp.tool() decorator | Auto-generates schemas from Python type hints |
| Message history management | Custom conversation storage | Database with indexed conversation_id | Needs pagination, search, efficient retrieval |

**Key insight:** MCP SDK handles complex tool orchestration (schema generation, validation, execution). OpenAI SDK handles LLM communication complexities. Focus implementation effort on business logic and integration.

## Common Pitfalls

### Pitfall 1: Cohere OpenAI Compatibility Endpoint Confusion
**What goes wrong:** Using incorrect base URL or unsupported Cohere models with OpenAI SDK
**Why it happens:** Cohere's OpenAI compatibility layer may have specific endpoint paths and model name requirements
**How to avoid:**
- Verify exact endpoint URL from Cohere documentation (current research shows uncertainty between `/v1` and `/compatibility/v1`)
- Test with simple chat completion before implementing full system
- Check which Cohere models support OpenAI-compatible interface
**Warning signs:** 404 errors, "model not found" errors, authentication failures despite valid API key

### Pitfall 2: MCP Transport Type Mismatch
**What goes wrong:** Using stdio transport in a web server context
**Why it happens:** MCP examples often show stdio transport (for Claude Desktop), but web servers need SSE or HTTP
**How to avoid:**
- Use `mcp.streamable_http_app()` for FastAPI mounting
- Never use stdio transport in production web servers
- stdio is only for desktop application integration (Claude Desktop)
**Warning signs:** Server hangs, broken pipe errors, clients can't connect

### Pitfall 3: Tool Execution Without Error Handling
**What goes wrong:** LLM requests tool execution, tool fails, entire chat breaks
**Why it happens:** Network errors, database failures, validation errors not caught
**How to avoid:**
- Wrap all MCP tool implementations with try-catch
- Return error objects instead of throwing exceptions
- LLM should receive structured error messages to inform user
**Warning signs:** 500 errors crash chat sessions, users get generic error messages

### Pitfall 4: Message History Context Window Overflow
**What goes wrong:** Sending entire conversation history to LLM exceeds token limits
**Why it happens:** Long conversations accumulate thousands of tokens
**How to avoid:**
- Implement sliding window (last N messages)
- Summarize older messages
- Calculate token count before API call
- Use Cohere's context window limits (varies by model)
**Warning signs:** "Maximum context length exceeded" errors, slow responses, high API costs

### Pitfall 5: Missing Authentication Between Chat and MCP Server
**What goes wrong:** MCP server exposes task operations without verifying user identity
**Why it happens:** MCP protocol doesn't inherently include authentication
**How to avoid:**
- Pass user context through MCP tool calls
- Validate user permissions in each tool implementation
- Include JWT or session token in MCP server context
**Warning signs:** Users can access/modify other users' tasks

## Code Examples

### Verified Pattern: OpenAI SDK Custom Endpoint
```python
# Source: OpenAI Python SDK official README
from openai import OpenAI

# Method 1: Direct configuration
client = OpenAI(
    base_url="https://api.cohere.ai/v1",  # To be verified
    api_key=os.getenv("COHERE_API_KEY")
)

# Method 2: Environment variable
# Set OPENAI_BASE_URL=https://api.cohere.ai/v1
client = OpenAI(api_key=os.getenv("COHERE_API_KEY"))

# Standard usage
response = client.chat.completions.create(
    model="command-r-plus",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Verified Pattern: MCP Tool Definition
```python
# Source: MCP Python SDK and modelcontextprotocol.io
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Todo Server")

@mcp.tool()
async def create_task(
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: str | None = None
) -> dict:
    """
    Create a new task in the todo list.

    Args:
        title: The task title (required)
        description: Optional task description
        priority: Task priority (low/medium/high)
        due_date: Optional due date in ISO format

    Returns:
        dict: Created task object with id, title, status
    """
    # Tool implementation
    # MCP automatically generates schema from type hints
    task = await task_service.create(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )
    return {"id": task.id, "title": task.title, "status": "created"}
```

### Verified Pattern: FastAPI MCP Mounting
```python
# Source: MCP Python SDK documentation
from fastapi import FastAPI
from mcp.server.mcpserver import MCPServer

app = FastAPI()

# Create MCP server
mcp = MCPServer("Todo MCP")

# Define tools (as above)
@mcp.tool()
async def list_tasks() -> list:
    """List all tasks"""
    return []

# Mount MCP server to FastAPI
# Uses SSE (Server-Sent Events) for browser compatibility
app.mount("/mcp", mcp.streamable_http_app())

# Regular FastAPI routes can coexist
@app.get("/health")
def health():
    return {"status": "ok"}
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Custom LLM API clients | OpenAI SDK with base_url | 2023-2024 | Standardized interface for multiple providers |
| Manual function calling | MCP protocol | 2024-2025 | Standardized tool integration across LLM platforms |
| Stdio-only MCP | Multiple transports (stdio/SSE/HTTP) | 2024-2025 | MCP usable in web applications, not just desktop |
| GPT-specific tools | Provider-agnostic tool definitions | 2024-2025 | Tools work across OpenAI, Anthropic, Cohere |

**Deprecated/outdated:**
- **OpenAI Functions API (deprecated)**: Replaced by Tools API with more structured format
- **Custom tool calling formats**: MCP provides standardized protocol
- **Direct Cohere SDK for chat**: OpenAI-compatible endpoint preferred for consistency

## Open Questions

### 1. Cohere OpenAI Compatibility Endpoint
**What we know:**
- Cohere offers OpenAI-compatible endpoints
- OpenAI Python SDK supports custom base_url configuration
- Endpoint likely at `https://api.cohere.ai/v1` or similar

**What's unclear:**
- Exact base URL path for OpenAI compatibility (`/v1` vs `/compatibility/v1`)
- Which Cohere models support OpenAI-compatible interface
- Whether all OpenAI SDK features (streaming, function calling) are supported
- Latest Cohere model names (command-r-plus confirmed, but command-a-03-2025 needs verification)

**Recommendation:**
- Start implementation with `https://api.cohere.ai/v1` and test with `command-r-plus` model
- Consult Cohere documentation at https://docs.cohere.com/docs/openai-compatibility before finalizing
- Have fallback to native Cohere SDK if compatibility issues arise
- Create integration test early to validate endpoint configuration

### 2. OpenAI ChatKit Package Availability
**What we know:**
- Research could not verify existence of `@openai/chatkit` npm package
- Multiple alternative React chat UI libraries exist
- Chat UI implementation is needed for frontend

**What's unclear:**
- Whether OpenAI officially provides a ChatKit package
- If it exists, what are its configuration options and API requirements
- Whether it supports custom backends or only OpenAI endpoints

**Recommendation:**
- Verify package existence: `npm search @openai/chatkit`
- If not found, use established alternatives:
  - `react-chatbot-kit` - Popular, well-documented
  - `@chatscope/chat-ui-kit-react` - Feature-rich, modern
  - Custom implementation using existing project UI components
- Custom implementation may provide better integration with existing design system

### 3. MCP Server Authentication Pattern
**What we know:**
- MCP focuses on tool definition and execution
- FastAPI integration is possible via ASGI mounting
- User context needed for multi-user todo application

**What's unclear:**
- Recommended pattern for passing authenticated user context to MCP tools
- Whether to embed auth in MCP layer or handle in FastAPI middleware
- How to prevent tool abuse/unauthorized access

**Recommendation:**
- Implement authentication at FastAPI layer before MCP
- Pass authenticated user_id as context to all MCP tool calls
- Create wrapper service that injects user context into MCP tools
- Document security model in implementation plan

### 4. Cohere Model Selection
**What we know:**
- Cohere offers multiple command models
- Different models have different capabilities and pricing
- Model names include: command-r-plus, command-r, possibly command-a-03-2025

**What's unclear:**
- Which model best balances cost and capability for chat
- Context window sizes for each model
- Function calling support across models
- Latest model releases and their features

**Recommendation:**
- Start with `command-r-plus` (known to be available and capable)
- Test function calling capabilities early
- Make model name configurable via environment variable
- Monitor Cohere releases for newer models

## Sources

### Primary (HIGH confidence)
- [Model Context Protocol Official Docs](https://modelcontextprotocol.io/introduction) - MCP architecture, transports, tool definition
- [MCP Build Server Guide](https://modelcontextprotocol.io/docs/develop/build-server) - Python server implementation patterns
- OpenAI Python SDK GitHub README - Custom base_url configuration

### Secondary (MEDIUM confidence)
- MCP Python SDK GitHub - FastAPI/ASGI integration hints
- OpenAI Python SDK documentation - Chat completions with custom endpoints

### Tertiary (LOW confidence - requires verification)
- Cohere OpenAI compatibility endpoint URL (multiple sources suggest `/v1` but not officially verified)
- OpenAI ChatKit package (could not verify existence)
- Specific Cohere model names for 2025-2026 (command-a-03-2025 not verified)

### Recommended Additional Verification
- [ ] Consult Cohere official documentation for OpenAI compatibility details
- [ ] Verify OpenAI ChatKit npm package existence and documentation
- [ ] Test Cohere endpoint with OpenAI SDK to confirm exact URL and model names
- [ ] Review MCP Python SDK source code for complete FastAPI integration examples

## Metadata

**Confidence breakdown:**
- **MCP Python SDK integration:** HIGH - Official documentation provides clear patterns
- **OpenAI SDK custom endpoint:** HIGH - Well-documented feature with examples
- **Cohere OpenAI compatibility:** MEDIUM - Concept confirmed but specific implementation details need verification
- **Frontend ChatKit:** LOW - Package existence unverified, alternatives exist
- **FastAPI + MCP integration:** MEDIUM - Documented but needs practical testing

**Research date:** 2026-02-06
**Valid until:** 2026-03-06 (30 days - stable technologies but LLM provider APIs evolve)

**Action items before implementation:**
1. Verify Cohere OpenAI compatibility endpoint URL and supported models
2. Test OpenAI SDK with Cohere endpoint to confirm integration works
3. Decide on chat UI library (verify ChatKit or select alternative)
4. Create proof-of-concept MCP server with FastAPI mounting
5. Design authentication flow for user-specific MCP tool access
