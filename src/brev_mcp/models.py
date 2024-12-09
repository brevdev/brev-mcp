from typing import Dict, List, Optional, Literal, Callable, Awaitable
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from mcp.types import Tool, TextContent

class Quota(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    maximum: Optional[int] = None
    current: Optional[int] = None
    unit: Optional[str] = None

class InstanceTypeQuota(BaseModel):
    on_demand: Optional[Quota] = Field(None, alias="onDemand")
    spot: Optional[Quota] = None
    reserved: Optional[Quota] = None

    class Config:
        populate_by_name = True

class InstanceTypePrice(BaseModel):
    instance_type_price_id: Optional[str] = Field(None, alias="instanceTypePriceId")
    operating_system: Optional[str] = Field(None, alias="operatingSystem")
    instance_type: Optional[str] = Field(None, alias="instanceType")
    term_type: Optional[str] = Field(None, alias="termType")
    term_attributes: Optional[Dict[str, str]] = Field(None, alias="termAttributes")
    unit: Optional[str] = None
    price_usd: Optional[str] = Field(None, alias="priceUsd")
    usage_type: Optional[str] = Field(None, alias="usageType")

    class Config:
        populate_by_name = True

class CurrencyAmount(BaseModel):
    currency: Optional[str] = None
    amount: Optional[str] = None

class Storage(BaseModel):
    count: Optional[int] = None
    size: Optional[str] = None
    type: Optional[str] = None
    min_size: Optional[str] = Field(None, alias="minSize")
    max_size: Optional[str] = Field(None, alias="maxSize")
    price_per_gb_hr: Optional[CurrencyAmount] = Field(None, alias="pricePerGbHr")

    class Config:
        populate_by_name = True

class Gpu(BaseModel):
    count: Optional[int] = None
    memory: Optional[str] = None
    manufacturer: Optional[str] = None
    name: Optional[str] = None
    network_details: Optional[str] = Field(None, alias="networkDetails")
    memory_details: Optional[str] = Field(None, alias="memoryDetails")

    class Config:
        populate_by_name = True

class WorkspaceGroupPlatform(str, Enum):
    NOOP = "noop"
    AWS = "aws"
    DEV_PLANE = "dev-plane"
    AWS_EC2_SPOT = "aws:ec2:spot"

class WorkspaceGroupStatus(str, Enum):
    DEPLOYING = "DEPLOYING"
    RUNNING = "RUNNING"
    DEPRECATED = "DEPRECATED"
    DELETING = "DELETING"
    FAILURE = "FAILURE"

class TenantType(str, Enum):
    SHARED = "shared"
    ISOLATED = "isolated"

class Metadata(BaseModel):
    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")
    deleted_at: Optional[datetime] = Field(None, alias="deletedAt")
    id: Optional[str] = None
    org_id: Optional[str] = Field(None, alias="orgId")

    class Config:
        populate_by_name = True

class Workspace(BaseModel):
    # Add workspace fields based on your needs
    pass

class WorkspaceGroup(BaseModel):
    metadata: Optional[Metadata] = None
    name: Optional[str] = None
    host: Optional[str] = None  # Assuming uri.Host is a string
    platform: Optional[WorkspaceGroupPlatform] = None
    platform_id: Optional[str] = Field(None, alias="platformId")
    platform_region: Optional[str] = Field(None, alias="platformRegion")
    platform_type: Optional[str] = Field(None, alias="platformType")
    usable_regions: Optional[List[str]] = Field(None, alias="usableRegions")
    status: Optional[WorkspaceGroupStatus] = None
    workspaces: Optional[List[Workspace]] = None
    tenant_type: Optional[TenantType] = Field(None, alias="tenantType")
    version: Optional[str] = None
    tags: Optional[Dict[str, List[str]]] = None

    class Config:
        populate_by_name = True

class Location(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    available: Optional[bool] = None
    endpoint: Optional[str] = None
    country: Optional[str] = None

class WorkspaceGroupWithLocations(WorkspaceGroup):
    locations: Optional[List[Location]] = None

class InstanceType(BaseModel):
    type: Optional[str] = None
    supported_gpus: Optional[List[Gpu]] = Field(None, alias="supportedGpus")
    supported_storage: Optional[List[Storage]] = Field(None, alias="supportedStorage")
    memory: Optional[str] = None
    maximum_network_interfaces: Optional[int] = Field(None, alias="maximumNetworkInterfaces")
    network_performance: Optional[str] = Field(None, alias="networkPerformance")
    supported_num_cores: Optional[List[int]] = Field(None, alias="supportedNumCores")
    default_cores: Optional[int] = Field(None, alias="defaultCores")
    vcpu: Optional[int] = None
    supported_architectures: Optional[List[str]] = Field(None, alias="supportedArchitectures")
    clock_speed_in_ghz: Optional[str] = Field(None, alias="clockSpeedInGhz")
    sub_location: Optional[str] = Field(None, alias="subLocation")
    prices: Optional[List[InstanceTypePrice]] = None
    default_price: Optional[str] = Field(None, alias="defaultPrice")
    elastic_root_volume: Optional[bool] = Field(None, alias="elasticRootVolume")
    supported_usage_classes: Optional[List[str]] = Field(None, alias="supportedUsageClasses")
    quota: Optional[InstanceTypeQuota] = None
    location: Optional[str] = None
    is_available: Optional[bool] = Field(None, alias="isAvailable")
    variable_price: Optional[bool] = Field(None, alias="variablePrice")
    rebootable: Optional[bool] = None
    preemptible: Optional[bool] = None
    base_price: Optional[CurrencyAmount] = Field(None, alias="basePrice")
    sub_location_type_changeable: Optional[bool] = Field(None, alias="subLocationTypeChangeable")
    estimated_deploy_time: Optional[str] = Field(None, alias="estimatedDeployTime")
    user_privilege_escalation_disabled: Optional[bool] = Field(None, alias="userPrivilegeEscalationDisabled")
    not_privileged: Optional[bool] = Field(None, alias="notPrivileged")
    is_container: Optional[bool] = Field(None, alias="isContainer")

    class Config:
        populate_by_name = True

class InstanceTypeWorkspaceGroup(InstanceType):
    workspace_groups: Optional[List[WorkspaceGroup]] = Field(None, alias="workspaceGroups")

    class Config:
        populate_by_name = True


class WorkspaceGroupError(BaseModel):
    workspace_group: Optional[WorkspaceGroup] = Field(None, alias="workspaceGroup")
    error_message: Optional[str] = Field(None, alias="errorMessage")

    class Config:
        populate_by_name = True


class AllInstanceTypeObj(BaseModel):
    all_instance_types: Optional[List[InstanceTypeWorkspaceGroup]] = Field(None, alias="allInstanceTypes")
    workspace_group_errors: Optional[List[WorkspaceGroupError]] = Field(None, alias="workspaceGroupErrors")

    class Config:
        populate_by_name = True

Workspace_Group_Ids: dict[str, str] = {
    "aws": "devplane-brev-1",
    "gcp": "GCP",
    "azure": "azure-dgxc-wg",
    "crusoe": "crusoe-brev-wg",
    "lambda-labs": "lambda-labs-test",
    "fluidstack": "FluidStack",
    "launchpad": "launchpad-test-wg",
    "akash": "akash-brev-wg",
    "gcpalpha": "dgxc-gcp",
}

class CloudProvider(str, Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    CRUSOE = "crusoe"
    LAMBDA_LABS = "lambda-labs"
    FLUIDSTACK = "fluidstack"
    LAUNCHPAD = "launchpad"
    AKASH = "akash"
    GCPALPHA = "gcpalpha"


    def get_workspace_group_id(self):
        return Workspace_Group_Ids[self.value]

DEFAULT_VERB_CONFIG = "build:\n  system_packages: []\n  python_version: '3.10'\n  cuda: 12.0.1\n  python_packages:\n    - jupyterlab\n  run:\n    - sh -c \"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\" \"\" --unattended\nuser:\n  shell: zsh\n  authorized_keys_path: /home/ubuntu/.ssh/authorized_keys\nports:\n  - '2222:22'\nservices:\n  - name: jupyter\n    entrypoint: jupyter-lab --ip=0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password=''\n    ports:\n      - '8888'"

class CreateWorkspaceRequest(BaseModel):
    # version: Optional[str] = None
    name: str
    # description: Optional[str] = None
    workspace_group_id: Optional[str] = Field(None, alias="workspaceGroupId")
    # workspace_template_id: Optional[str] = Field(None, alias="workspaceTemplateId")
    # workspace_class: Optional[WorkspaceClassID] = Field(None, alias="workspaceClassId")
    # git_repo: Optional[str] = Field(None, alias="gitRepo")
    # is_stoppable: Optional[bool] = Field(None, alias="isStoppable")
    # tunnel: Optional[WorkspaceTunnel] = None
    # primary_application_id: Optional[str] = Field(None, alias="primaryApplicationId")
    # startup_script: Optional[str] = Field(None, alias="startupScript")
    # startup_script_path: Optional[str] = Field(None, alias="startupScriptPath")
    # ide_config: Optional[ClientConfig] = Field(None, alias="ideConfig")
    # dont_check_ssh_keys: bool = Field(False, alias="dontCheckSSHKeys")
    # repos: ReposV0
    # execs: ExecsV0
    # init_branch: Optional[str] = Field(None, alias="initBranch")
    # dot_brev_path: Optional[str] = Field(None, alias="dotBrevPath")
    # repos_v1: Optional[ReposV1] = Field(None, alias="reposV1")
    # execs_v1: Optional[ExecsV1] = Field(None, alias="execsV1")
    instance_type: Optional[str] = Field(None, alias="instanceType")
    # disk_storage: Optional[str] = Field(None, alias="diskStorage")
    # region: Optional[str] = None
    # image: Optional[str] = None
    # architecture: Optional[Architecture] = None
    # spot: bool = False
    # on_container: bool = Field(False, alias="onContainer")
    # initial_container_image: Optional[str] = Field(None, alias="containerImage")
    verb_yaml: Optional[str] = Field(DEFAULT_VERB_CONFIG, alias="verbYaml")
    # base_image: Optional[str] = Field(None, alias="baseImage")
    # custom_container: Optional[CustomContainer] = Field(None, alias="customContainer")
    # port_mappings: Optional[Dict[str, str]] = Field(None, alias="portMappings")
    workspace_version: Optional[Literal["v1", "v0"]] = Field("v1", alias="workspaceVersion")
    # retry_for: Optional[str] = Field(None, alias="retryFor")
    # vm_only_mode: bool = Field(False, alias="vmOnlyMode")
    # files: Optional[List[FileRequest]] = None
    # labels: Optional[Dict[str, str]] = None
    # launch_jupyter_on_start: bool = Field(False, alias="launchJupyterOnStart")

    class Config:
        populate_by_name = True

class WorkspaceStatus(str, Enum):
    DEPLOYING = "DEPLOYING"
    STARTING = "STARTING"
    RUNNING = "RUNNING"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    DELETING = "DELETING"
    FAILURE = "FAILURE"

class HealthStatus(str, Enum):
    UNSPECIFIED = "" 
    HEALTHY = "HEALTHY"
    UNHEALTHY = "UNHEALTHY"
    UNAVAILABLE = "UNAVAILABLE"

class ServiceType(str, Enum):
    SSH = "SSH"
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    TCP = "TCP"
    RDP = "RDP"

class WorkspaceCapability(str, Enum):
    STOP_START_INSTANCE = "stop-start-instance"
    AUTOSTOP = "autostop"
    EXPOSE_PUBLIC_PORTS = "expose-public-ports"
    CLONE = "clone"
    RETIRE_VOLUME = "retire-volume"
    MACHINE_IMAGE = "machine-image"
    MODIFY_FIREWALL = "modify-firewall"
    INSTANCE_USER_DATA = "instance-userdata"
    VPC_SUBNETS = "vpc-subnets"
    CONTAINER_CLOUD = "container-cloud"


class VerbBuildStatus(str, Enum):
    UNSPECIFIED = ""
    CREATE_FAILED = "CREATE_FAILED"
    PENDING = "PENDING"
    BUILDING = "BUILDING"
    COMPLETED = "COMPLETED"

class FileType(str, Enum):
    COLAB = "colab"
    NOTEBOOK = "notebook"
    GITHUB = "github"
    GITLAB = "gitlab"

class WorkspaceStartStatus(str, Enum):
    UNSPECIFIED = ""
    STARTING = "STARTING"
    FAILURE = "FAILURE"
    STARTED = "STARTED"

class WorkspaceVersion(str, Enum):
    UNSPECIFIED = ""
    V0 = "v0"
    V1 = "v1"

class WorkspaceApplicationAPIKey(BaseModel):
    enabled: bool
    id: str
    client_id: str = Field(alias="clientID")
    client_secret: str = Field(alias="clientSecret")

class WorkspaceApplicationPolicy(BaseModel):
    allowed_user_auth_ids: List[str] = Field(alias="allowedUserAuthIDs")
    allow_everyone: bool = Field(alias="allowEveryone")
    api_key: WorkspaceApplicationAPIKey = Field(alias="apiKey")
    allowed_user_provider_ids: List[str] = Field(alias="allowedUserProviderIDs")

class WorkspaceApplication(BaseModel):
    cloudflare_application_id: str = Field(alias="cloudflareApplicationID")
    cloudflare_dns_record_id: str = Field(alias="cloudflareDnsRecordID")
    hostname: str
    name: str
    service_type: ServiceType = Field(alias="serviceType")
    port: int
    application_setup_bash: str = Field(alias="userApplicationSetupBash")
    policy: WorkspaceApplicationPolicy
    health_check_id: str = Field(alias="healthCheckID")

class WorkspaceTunnel(BaseModel):
    tunnel_id: str = Field(alias="tunnelID")
    applications: List[WorkspaceApplication]
    tunnel_setup_bash: str = Field(alias="tunnelSetupBash")
    tunnel_status: HealthStatus = Field(alias="tunnelStatus")

class Thresholds(BaseModel):
    failure_threshold: int = Field(alias="failureThreshold")
    success_threshold: int = Field(alias="successThreshold")

class Timestamp(BaseModel):
    seconds: int
    nanos: int

class HealthCheck(BaseModel):
    health_check_id: str = Field(alias="healthCheckId")
    create_time: Optional[Timestamp] = Field(alias="createTime")
    update_time: Optional[Timestamp] = Field(alias="updateTime")
    labels: Dict[str, str]
    status: str
    thresholds: Optional[Thresholds] = None

class FileMetadata(BaseModel):
    type: FileType

class FileObject(BaseModel):
    url: str
    path: str
    metadata: FileMetadata

class ClientConfig(BaseModel):
    # Add fields based on data.ClientConfig
    pass

class ReposV0(BaseModel):
    # Add fields based on data.ReposV0
    pass

class ExecsV0(BaseModel):
    # Add fields based on data.ExecsV0
    pass

class ReposV1(BaseModel):
    # Add fields based on data.ReposV1
    pass

class ExecsV1(BaseModel):
    # Add fields based on data.ExecsV1
    pass

class CustomContainer(BaseModel):
    # Add fields based on data.CustomContainer
    pass

class WorkspaceTemplateJSON(BaseModel):
    # Add fields based on WorkspaceTemplateJSON
    pass

class Workspace(BaseModel):
    id: str
    workspace_group_id: str = Field(alias="workspaceGroupId")
    organization_id: str = Field(alias="organizationId")
    name: str
    description: str
    created_by_user_id: str = Field(alias="createdByUserId")
    dns: Optional[str] = None
    password: Optional[str] = None
    workspace_class: str = Field(alias="workspaceClassId")
    git_repo: Optional[str] = Field(None, alias="gitRepo")
    workspace_template: WorkspaceTemplateJSON = Field(alias="workspaceTemplate")
    status: WorkspaceStatus
    status_message: str = Field(alias="statusMessage")
    health_status: HealthStatus = Field(alias="healthStatus")
    last_online_at: str = Field(alias="lastOnlineAt")
    created_at: str = Field(alias="createdAt")
    updated_at: str = Field(alias="updatedAt")
    version: str
    ssh_port: int = Field(alias="sshPort")
    ssh_user: str = Field(alias="sshUser")
    ssh_proxy_hostname: str = Field(alias="sshProxyHostname")
    host_ssh_port: int = Field(alias="hostSshPort")
    host_ssh_user: str = Field(alias="hostSshUser")
    host_ssh_proxy_hostname: str = Field(alias="hostSshProxyHostname")
    on_container: bool = Field(alias="onContainer")
    is_stoppable: bool = Field(alias="isStoppable")
    tunnel: Optional[WorkspaceTunnel] = None
    primary_application_id: Optional[str] = Field(None, alias="primaryApplicationId")
    startup_script: str = Field(alias="startupScript")
    startup_script_path: str = Field(alias="startupScriptPath")
    init_branch: str = Field(alias="initBranch")
    dot_brev_path: str = Field(alias="dotBrevPath")
    network_id: str = Field(alias="networkId")
    ide_config: ClientConfig = Field(alias="ideConfig")
    # repos: ReposV0
    # execs: ExecsV0
    repos_v1: Optional[ReposV1] = Field(None, alias="reposV1")
    execs_v1: Optional[ExecsV1] = Field(None, alias="execsV1")
    stop_timeout: Optional[int] = Field(None, alias="stopTimeout")
    instance_type: str = Field(alias="instanceType")
    disk_storage: str = Field(alias="diskStorage")
    image: str
    region: str
    exposed_ports: List[int] = Field(alias="exposedPorts")
    spot: bool
    workspace_capabilities: List[WorkspaceCapability] = Field(alias="workspaceCapabilities")
    workspace_image_uri: str = Field(alias="workspaceImageUri")
    verb_yaml: str = Field(None, alias="verbYaml")
    verb_build_status: VerbBuildStatus = Field(alias="verbBuildStatus")
    health_checks: Optional[List[HealthCheck]] = Field(alias="healthCheck")
    file_objects: Optional[Dict[str, FileObject]] = Field(None, alias="fileObjects")
    additional_users: Optional[List[str]] = Field(None, alias="additionalUsers")
    base_image: Optional[str] = Field(None, alias="baseImage")
    port_mappings: Optional[Dict[str, str]] = Field(None, alias="portMappings")
    last_start_status: WorkspaceStartStatus = Field(alias="lastStartStatus")
    last_start_status_message: str = Field(alias="lastStartStatusMessage")
    workspace_version: WorkspaceVersion = Field(alias="workspaceVersion")
    vm_only_mode: bool = Field(alias="vmOnlyMode")
    custom_container: Optional[CustomContainer] = Field(None, alias="customContainer")
    instance_type_info: Optional[InstanceType] = Field(None, alias="instanceTypeInfo")

    class Config:
        populate_by_name = True

class CredentialsFile(BaseModel):
    access_token: str
    refresh_token: str

class ActiveOrgFile(BaseModel):
    id: str
    name: str
    userNetworkId: str

class ToolModel(BaseModel):
    tool: Tool
    call_tool: Callable[..., Awaitable[TextContent]]