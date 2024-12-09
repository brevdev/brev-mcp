import logging
from typing import Any
from collections.abc import Sequence
from .instance_types import get_instance_types
from .models import CloudProvider
from .tools import tool_models

from mcp.server.models import InitializationOptions
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource
)
from mcp.server import NotificationOptions, Server
from pydantic import AnyUrl
import mcp.server.stdio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("brev-server")

app = Server("brev_mcp")

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available Brev resources."""
    return [
        Resource(
            uri=f"brev://instance-types/{provider.value}",
            name=f"{provider.value} Instance Types",
            mimeType="application/json",
            description=f"Available virtual machine instance types for Brev provider {provider.value}",
        )
        for provider in CloudProvider
    ]

@app.read_resource()
async def read_resource(uri: AnyUrl) -> str:
    """Read resource content."""
    if str(uri).startswith("brev://instance-types/"):
        provider = CloudProvider(str(uri).split("/")[-1])
    else:
        raise ValueError(f"Unknown resource: {uri}")


    instance_types = await get_instance_types(provider)
    return instance_types

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available brev tools."""
    return [tool_model.tool for _, tool_model in tool_models.items()]

@app.call_tool()
async def call_tool(tool_name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
    """Handle brev tool calls"""
    if tool_name not in tool_models:
        raise ValueError(f"Unknown tool: {tool_name}")

    if not isinstance(arguments, dict):
        raise ValueError(f"Invalid {tool_name} arguments")
    
    return await tool_models[tool_name].call_tool(arguments)

# TO DO: aws instance types response is too long: result exceeds maximum length of 1048576
# TO DO: should have a tool call that can filter based on providers -> doing a query like "I'll help you find all single H100 instances across the cloud providers."
# requires a bunch of api calls
# TO DO: Error executing code: MCP error -2: Request timed out
# TO DO: handle notifications
async def main():
    # Run the server using stdin/stdout streams
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="brev_mcp",
                server_version="0.1.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )