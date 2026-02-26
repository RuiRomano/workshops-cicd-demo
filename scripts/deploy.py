import argparse
import sys
from azure.identity import InteractiveBrowserCredential, AzureCliCredential
from fabric_cicd import FabricWorkspace, publish_all_items

parser = argparse.ArgumentParser(description="Deploy PBIP to Fabric")
parser.add_argument("--workspace_name", type=str, required=False, help="Target workspace Name", default="Workshop - Lab 2")
parser.add_argument("--environment", type=str, default="DEV", help="Environment name")
parser.add_argument("--spn-auth", type=bool, default=False, help="Use SPN authentication")
args = parser.parse_args()

# Authentication (SPN or Interactive)

if (not args.spn_auth):
    credential = InteractiveBrowserCredential()
else:
    # Check current login: az account show
    credential = AzureCliCredential()

workspace_params = {
    "workspace_name": args.workspace_name,
    "environment": args.environment,
    "repository_directory": "./src",
    "item_type_in_scope": ["SemanticModel", "Report"],
    "token_credential": credential,
}

target_workspace = FabricWorkspace(**workspace_params)

publish_all_items(target_workspace)