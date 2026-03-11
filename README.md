# Workshop CICD Demo

This repository demonstrates a CI/CD pipeline example for the workshop lab, showcasing automated deployment and quality assurance workflows.

## CI/CD Flow

The pipeline implements two main workflows:

### Production Deployment
- **Trigger**: Push to `main` branch
- **Action**: Automatic deployment to **PRD** (Production) environment

### Development & Quality Assurance
- **Trigger**: Pull Request creation/update
- **Actions**: 
  - Deployment to **DEV** environment
  - Best practice analysis against source reports and models


## Repository Structure

```text
repo/
├── .github/
│   └── workflows/
│       ├── deploy.yml                ← deployment workflow
│       └── bpa.yml                   ← quality checks workflow
├── src/                              ← Power BI project files (PBIP)
│   ├── Sales.Report/
│   ├── Sales.SemanticModel/
│   ├── AnotherReport.Report/
│   ├── Sales.pbip
│   └── parameter.yml                 ← environment parameterization
├── scripts/
│   ├── deploy.py                     ← deployment script
│   ├── deploy.config                 ← workspace name configuration (for CI/CD)
│   └── bpa/                          ← BPA scripts and rule files
│       ├── bpa.ps1
│       ├── bpa-rules-semanticmodel.json
│       └── bpa-rules-report.json
├── requirements.txt                  ← Python dependencies
└── .gitignore
```

### Understanding `scripts/deploy.py`

The script accepts three command-line arguments:

| Argument | Purpose |
| --- | --- |
| `--workspace_name` | Target Fabric workspace name. If omitted, the script resolves it from configuration files (see below). |
| `--environment` | An environment label (`DEV` or `PRD`). Used by `fabric-cicd` to apply the correct values from `parameter.yml`. Defaults to `DEV`. |
| `--spn-auth` | When `True`, authenticates via the Azure CLI session (service principal — used in GitHub Actions). When `False` (default), opens a **browser window for interactive login** — this is what you use locally. |

### Configuration file `deploy.config`

The script resolves the target workspace name in this order of priority:

| Priority | Source                          | Committed to Git? | Purpose                                                   |
| -------- | ------------------------------- | ----------------- | --------------------------------------------------------- |
| 1        | `--workspace_name` CLI argument | n/a               | Explicit override for one-off runs                        |
| 2        | `scripts/deploy.config`         | **Yes**           | Shared workspace configuration used by CI/CD and the team |

[**`scripts/deploy.config`**](scripts/deploy.config) is the main configuration file. It is committed to the repository and used by GitHub Actions. Edit this file to set the workspace names that the team and CI/CD pipeline should use.

```ini
PBI_WORKSPACE_DEV=Workshop - Lab 2 (DEV)
PBI_WORKSPACE_PRD=Workshop - Lab 2 (PRD)
```

> [!IMPORTANT]
> * The target workspaces **must already exist** in Microsoft Fabric before you can deploy to them. `fabric-cicd` does not create workspaces — it only publishes items to existing ones.


## Run fabric-cicd Locally

1. Install [Python 3.13](https://apps.microsoft.com/detail/9pnrbtzxmb4z)	

2. Install dependencies from the repository root:

	```bash
	python -m pip install -r requirements.txt
	```

3. Run deployment to DEV environment (default authentication is interactive browser login):

	```bash
	python scripts/deploy.py
	```

	Other examples:
	
	```bash
	# Explicit environment override
	python scripts/deploy.py --environment PRD

	# Explicit override (takes precedence over environment mapping)
	python scripts/deploy.py --environment DEV --workspace_name "My Custom Workspace"

	# Advanced: use Azure CLI auth instead of system-browser interactive auth
	az login
	python scripts/deploy.py --spn-auth True --environment DEV
	```

## Run BPA Locally

From the repository root, run:

```bash
pwsh -File scripts/bpa/bpa.ps1 -src @("src")
```

On Windows PowerShell (if `pwsh` is not available), use:

```powershell
powershell -File scripts\bpa\bpa.ps1 -src @("src")
```