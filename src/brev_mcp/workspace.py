import json
from .api import create_workspace
from .models import (
    CloudProvider,
    CreateWorkspaceRequest
)

async def create_provider_workspace(name: str, cloud_provider: CloudProvider, instance_type: str) -> str:
    req = CreateWorkspaceRequest(
        name=name,
        workspaceGroupId=cloud_provider.get_workspace_group_id(),
        instanceType=instance_type,
    )
    workspace = await create_workspace(req)
    return json.dumps(workspace.model_dump(), indent=2)