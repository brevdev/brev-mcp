from brev_mcp import server

async def test_read_resource():
    instance_types = await server.read_resource("brev://instance-types/crusoe")
    print(instance_types)

async def test_get_instance_types_tool():
    tool_output = await server.call_tool("get_instance_types", {"cloud_provider": "crusoe"})
    print(tool_output[0].text)

async def test_create_workspace_tool():
    tool_output = await server.call_tool("create_workspace", {
        "name": "test-workspace-2",
        "cloud_provider": "crusoe",
        "instance_type": "l40s-48gb.1x"
    })
    print(tool_output[0].text)


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_get_instance_types_tool())