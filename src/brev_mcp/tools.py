from mcp.types import (
    TextContent,
    Tool
)
from .models import CloudProvider, ToolModel
from .instance_types import get_provider_instance_types
from .workspace import create_provider_workspace


async def get_instance_types_tool(args: dict[str, str]) -> TextContent:
    if "cloud_provider" not in args:
        raise ValueError("cloud_provider argument is required for get_instance_types tool")

    cloud_provider = CloudProvider(args["cloud_provider"])
    instance_types = await get_provider_instance_types(cloud_provider)
    return [
        TextContent(
            type="text", 
            text=instance_types
        )
    ]

async def create_workspace_tool(args: dict[str, str]) -> TextContent:
    if "name" not in args or "cloud_provider" not in args or "instance_type" not in args:
        raise ValueError("missing required arguments for create_workspace tool")

    cloud_provider = CloudProvider(args["cloud_provider"])
    workspace = await create_provider_workspace(args["name"], cloud_provider, args["instance_type"])
    return [
        TextContent(
            type="text", 
            text=workspace
        )
    ]


tool_models = {
    "get_instance_types": ToolModel(
        tool=Tool(
            name="get_instance_types",
            description="Get available instances types for a cloud provider",
            inputSchema={
                "type": "object",
                "properties": {
                    "cloud_provider": {
                        "description": "The cloud provider to get instance types for",
                        "enum": [provider.value for provider in CloudProvider]
                    }
                },
                "required": ["cloud_provider"]
            }
        ),
        call_tool=get_instance_types_tool
    ),
    "create_workspace": ToolModel(
        tool=Tool(
            name="create_workspace",
            description="Create a workspace from an instance type and cloud provider",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "description": "The name of the workspace",
                        "type": "string",
                    },
                    "cloud_provider": {
                        "description": "The cloud provider for the workspace",
                        "enum": [provider.value for provider in CloudProvider]
                    },
                    "instance_type": {
                        "description": "The instance type of the workspace",
                        "type": "string",
                    }
                },
                "required": ["cloud_provider"]
            }
        ),
        call_tool=create_workspace_tool
    )
}