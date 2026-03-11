
## CI/CD Behavior

- Pull requests targeting `main` deploy with environment `DEV`
- Pushes to `main` deploy with environment `PRD`
- Manual runs (`workflow_dispatch`) use the selected environment input

## Repository Structure

| File/Folder       | Purpose                                                      |
|-------------------|--------------------------------------------------------------|
| `.github/`        | GitHub Actions workflows and GitHub-specific files           |
| `.vscode/`        | VS Code settings and recommended extensions                  |
| `scripts/`        | Helper scripts for automation and deployment                 |
| `src/`            | Main Power BI project files and resources                    |
| `.gitignore`      | Specifies files/folders to be ignored by Git                 |

## Local Run

1. Install [Python 3.13](https://apps.microsoft.com/detail/9pnrbtzxmb4z)	

2. Install dependencies from the repository root:

	```bash
	python -m pip install -r requirements.txt
	```

3. Run deployment to DEV environment (default authentication is interactive browser login):

	```bash
	python scripts/deploy.py
	```

## Workspace Resolution Logic

`scripts/deploy.py` resolves the target workspace in this order:

1. `--workspace_name` (always highest priority)
2. `PBI_WORKSPACE_<ENV>` from `.env` in current working directory
3. `PBI_WORKSPACE_<ENV>` from `scripts/deploy.config`
4. Fail due to missing configuration

Examples:

```bash
# Deploy to PRD
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