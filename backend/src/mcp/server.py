"""MCP server for exposing task operation tools to AI agent."""
import asyncio
from modelcontextprotocol.server import Server
from modelcontextprotocol.transports.stdio import StdioTransport
from modelcontextprotocol.server.server_methods import TextContentServerMethods
from ..mcp import tools
import json


async def create_mcp_server():
    """Create and configure MCP server with task operation tools."""
    server = Server("todo-ai-server")

    # Register task operation tools as MCP resources
    # These will be exposed to the AI agent through MCP protocol
    pass


async def main():
    """Main entry point for MCP server."""
    server = await create_mcp_server()

    # Use stdio transport to communicate with AI agent
    transport = StdioTransport()
    await server.start(transport)

    try:
        # Keep server running
        await asyncio.Future()  # Runs forever until interrupted
    except KeyboardInterrupt:
        print("Shutting down MCP server...")
    finally:
        await server.shutdown()


if __name__ == "__main__":
    asyncio.run(main())