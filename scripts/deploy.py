"""
Deployment script for publishing PBIP artifacts to Microsoft Fabric.

Workspace resolution logic (in precedence order)
===============================================

1) Explicit CLI override (highest priority)
     - If `--workspace_name` is provided, that value is always used.

2) Environment-derived workspace via environment variables
     - If `--workspace_name` is not provided and `--environment` is provided,
         the script looks for `PBI_WORKSPACE_<ENV>` where `<ENV>` is the uppercased
         environment name.
     - Examples:
         - `--environment PRD` -> reads `PBI_WORKSPACE_PRD`
         - `--environment DEV` -> reads `PBI_WORKSPACE_DEV`
     - If the variable exists and is non-empty, it is used.

3) Fallback dictionary in script
     - If no environment is supplied and no `--workspace_name` is supplied,
         the script falls back to a hard-coded dictionary maintained here.
     - The default fallback environment key is `DEV`.

4) Additional safe fallback
     - If `--environment` is supplied but `PBI_WORKSPACE_<ENV>` is not defined,
         the script will try the hard-coded dictionary for that environment key.
     - If no mapping exists, execution fails with a clear error message.

Optional .env support
=====================

- The script attempts to load an optional `.env` file from repository root
        (one level above `scripts/`) using `python-dotenv`.
- Existing process environment variables are not overridden by `.env` values.
- Example keys in `.env`:
    - `PBI_WORKSPACE_DEV=Workshop - Lab 2`
    - `PBI_WORKSPACE_PRD=Workshop - Production`
"""

import argparse
import os
import sys
from pathlib import Path
from azure.identity import InteractiveBrowserCredential, AzureCliCredential
from dotenv import load_dotenv
from fabric_cicd import FabricWorkspace, publish_all_items


FALLBACK_WORKSPACE_BY_ENV = {
        "DEV": "Workshop - Lab 2 (DEV)",
        "PRD": "Workshop - Lab 2",
}
DEFAULT_FALLBACK_ENV = "DEV"


def load_dotenv_from_repo_root() -> None:
        repo_root = Path(__file__).resolve().parent.parent
        dotenv_path = repo_root / ".env"
        load_dotenv(dotenv_path=dotenv_path, override=False)


def resolve_workspace_name(explicit_workspace_name: str | None, environment_name: str | None) -> str:
        if explicit_workspace_name:
                return explicit_workspace_name

        normalized_environment = (environment_name or "").strip().upper()

        if normalized_environment:
                env_var_name = f"PBI_WORKSPACE_{normalized_environment}"
                workspace_name = os.getenv(env_var_name)
                if workspace_name:
                        return workspace_name

                fallback_workspace_name = FALLBACK_WORKSPACE_BY_ENV.get(normalized_environment)
                if fallback_workspace_name:
                        return fallback_workspace_name

                print(
                        f"Unable to resolve workspace for environment '{normalized_environment}'. "
                        f"Set {env_var_name} or add '{normalized_environment}' to FALLBACK_WORKSPACE_BY_ENV.",
                        file=sys.stderr,
                )
                sys.exit(1)

        return FALLBACK_WORKSPACE_BY_ENV[DEFAULT_FALLBACK_ENV]


parser = argparse.ArgumentParser(description="Deploy PBIP to Fabric")
parser.add_argument("--workspace_name", type=str, required=False, help="Target workspace name")
parser.add_argument("--environment", type=str, required=False, help="Environment name")
parser.add_argument("--spn-auth", type=bool, default=False, help="Use SPN authentication")
args = parser.parse_args()

load_dotenv_from_repo_root()
resolved_workspace_name = resolve_workspace_name(args.workspace_name, args.environment)
resolved_environment = args.environment or DEFAULT_FALLBACK_ENV

# Authentication (SPN or Interactive)

if (not args.spn_auth):
    credential = InteractiveBrowserCredential()
else:
    # Check current login: az account show
    credential = AzureCliCredential()

workspace_params = {
    "workspace_name": resolved_workspace_name,
    "environment": resolved_environment,
    "repository_directory": "./src",
    "item_type_in_scope": ["SemanticModel", "Report"],
    "token_credential": credential,
}

target_workspace = FabricWorkspace(**workspace_params)

publish_all_items(target_workspace)