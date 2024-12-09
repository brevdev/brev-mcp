import json
import logging
from typing import List

from .models import (
    CloudProvider,
    AllInstanceTypeObj,
    InstanceType,
)
from .api import get_instance_types 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("instance-types")


async def get_provider_instance_types(provider: CloudProvider)-> str:
    try:
        all_instance_types_obj = await get_instance_types()
        instance_types = filter_instance_types(all_instance_types_obj)
        for cloud_provider, instance_type_list in instance_types.items():
            logger.info(f"Number of instance types for {cloud_provider.value}: {len(instance_type_list)}")
        if provider not in instance_types:
            raise ValueError(f"Provider {provider.value} not found in instance types")
        instance_type_dicts = [
            instance_type.model_dump(exclude_none=True) 
            for instance_type in instance_types[provider]
        ] 
        return json.dumps(instance_type_dicts, indent=2)
    except Exception as e:
        logger.error(f"Error getting instance types: {str(e)}")
        raise RuntimeError(f"Failed to get instance types: {str(e)}")
    
def filter_instance_types(all_instance_types: AllInstanceTypeObj) -> dict[CloudProvider, List[InstanceType]]:
    instance_types: dict[CloudProvider, List[InstanceType]]= {}
    for it_wg in all_instance_types.all_instance_types:
        if len(it_wg.workspace_groups) == 0:
            continue
        cloud_provider = CloudProvider(it_wg.workspace_groups[0].platform_type)
        instance_type_data = it_wg.model_dump(exclude={'workspace_groups'})
        instance_type = InstanceType.model_validate(instance_type_data)

        if not instance_type:
            logger.warning(f"Instance type {it_wg.type} has no attributes")
            continue
        if cloud_provider not in instance_types:
            instance_types[cloud_provider] = [instance_type]
        else:
            instance_types[cloud_provider].append(instance_type)
    return instance_types