import httpx
from pydantic import ValidationError

from .models import (
    AllInstanceTypeObj,
    CreateWorkspaceRequest,
    Workspace
)
from .cli import get_acess_token, get_active_org_id

BASE_API_URL = "https://brevapi.us-west-2-prod.control-plane.brev.dev/api"

async def get_instance_types() -> AllInstanceTypeObj:
    access_token = get_acess_token() 
    org_id = get_active_org_id()
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(25.0)) as client:
            response = await client.get(
                f"{BASE_API_URL}/instances/alltypesavailable/{org_id}",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
            )
            response.raise_for_status()
            data = response.json()
            all_instance_types_obj = AllInstanceTypeObj.model_validate(data)
            return all_instance_types_obj
    except ValidationError as e:    
        raise RuntimeError(f"Failed to validate instance types: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to get instance types: {str(e)}")

async def create_workspace(request: CreateWorkspaceRequest) -> Workspace:
    access_token = get_acess_token() 
    org_id = get_active_org_id()
    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(25.0)) as client:
            json = request.model_dump(by_alias=True)
            response = await client.post(
                f"{BASE_API_URL}/organizations/{org_id}/workspaces",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json"
                },
                json=json            
            )
            response.raise_for_status()
            data = response.json()
            workspace = Workspace.model_validate(data)
            return workspace
    except ValidationError as e:    
        raise RuntimeError(f"Failed to validate workspace: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to create workspace: {str(e)}")