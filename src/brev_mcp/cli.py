import os
import json
from .models import CredentialsFile, ActiveOrgFile

CREDENTIALS_FILEPATH = "~/.brev/credentials.json"

ACTIVEORG_FILEPATH = "~/.brev/active_org.json"

def get_acess_token() -> str:
    env_token = os.getenv("BREV_API_TOKEN")
    if env_token:
        return env_token

    credentials_path = os.path.expanduser(CREDENTIALS_FILEPATH)

    if not os.path.exists(credentials_path):
        raise RuntimeError(f"brev credentials file {CREDENTIALS_FILEPATH} not found")
    
    with open(credentials_path, "r") as f:
        credentials = json.load(f)
        credential_file = CredentialsFile.model_validate(credentials)
        return credential_file.access_token
    
def get_active_org_id() -> str:
    env_org_id = os.getenv("BREV_ORG_ID")
    if env_org_id:
        return env_org_id

    activeorg_path = os.path.expanduser(ACTIVEORG_FILEPATH)

    if not os.path.exists(activeorg_path):
        raise RuntimeError(f"brev active org file {ACTIVEORG_FILEPATH} not found")
    
    with open(activeorg_path, "r") as f:
        active_org = json.load(f)
        active_org_file = ActiveOrgFile.model_validate(active_org)
        return active_org_file.id