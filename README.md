# workshops-cicd-demo

Sample repository to manage and deploy Power BI / Microsoft Fabric artifacts with GitHub Actions and `fabric-cicd`.

## Prerequisites

- [Python 3.12](https://www.python.org/downloads/release/python-3120/)
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- Access to the target Microsoft Fabric workspaces

## Quick Start

1. Install dependencies from the repository root:

	```bash
	python -m pip install -r requirements.txt
	```

2. (Optional) Create a `.env` file in repository root:

	```dotenv
	PBI_WORKSPACE_DEV=Workshop - Lab 2
	PBI_WORKSPACE_PRD=Workshop - Production
	```

3. Run deployment to DEV environment (default authentication is interactive browser login):

	```bash
	python scripts/deploy.py
	```

4. (Advanced, optional) If you want to use Azure CLI authentication instead of browser-based login:

	```bash
	az login
	python scripts/deploy.py --spn-auth True --environment DEV
	```

## First Deploy Checklist

Use this checklist for a smooth first run:

- [ ] You are in the repository root
- [ ] `python --version` shows Python 3.12.x
- [ ] `python -m pip install -r requirements.txt` completed successfully
- [ ] (Optional) `.env` exists with `PBI_WORKSPACE_DEV` / `PBI_WORKSPACE_PRD`
- [ ] Deployment command completed without errors

Quick verification commands:

```bash
python --version
python scripts/deploy.py --environment DEV
```

## Troubleshooting

### `pip` missing (`No module named pip`)

Use one of these options:

```bash
# Option 1 (preferred on Linux): install pip for Python 3 via OS package manager
sudo apt-get install -y python3-pip
python3 -m pip install -r requirements.txt
```

```bash
# Option 2: bootstrap pip directly
curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python3 /tmp/get-pip.py --user
python3 -m pip install --user -r requirements.txt
```

### Azure CLI authentication (advanced)

By default, `scripts/deploy.py` uses interactive authentication via the system browser.

Use Azure CLI auth only when needed:

```bash
az login
python3 scripts/deploy.py --spn-auth True --environment DEV
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
python3 scripts/deploy.py --environment PRD

# Explicit override (takes precedence over environment mapping)
python3 scripts/deploy.py --environment DEV --workspace_name "My Custom Workspace"

# Advanced: use Azure CLI auth instead of system-browser interactive auth
az login
python3 scripts/deploy.py --spn-auth True --environment DEV
```

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

This repository is organized to help you manage your Power BI project efficiently, especially if you are new to Git, GitHub, and automation with GitHub Actions. Here is a quick guide to the main folders and files you will find:

### `.github/`

Holds GitHub-specific files, including workflows for [GitHub Actions](https://docs.github.com/actions). These workflows automate tasks like testing, building, or deploying your project whenever you push changes to the repository.

**Workflow files in `.github/workflows/`:**

| File                | Purpose                                                                 |
|---------------------|-------------------------------------------------------------------------|
| `workflows/deploy.yml`        | Deploys the Power BI/Fabric artifacts to a target workspace and environment. **Triggered on pushes to `main` or manually via workflow dispatch**. Uses a Python deployment script and the `fabric-cicd` library. |
| `workflows/bpa.yml`           | Runs static analysis (Best Practice Analyzer) on semantic models and reports using community tools. **Triggered on pull requests to `main` or manually**. Helps enforce best practices before merging changes. |
| `dependabot.yml`    | Configures [Dependabot](https://docs.github.com/code-security/dependabot) to automate dependency updates, such as for devcontainer definitions. Not a workflow, but part of GitHub automation. |

### `.vscode/`

Contains settings and recommended extensions for [Visual Studio Code](https://code.visualstudio.com/). This helps standardize the development environment for all contributors.

### `scripts/`

This folder includes helper scripts (such as Python or shell scripts) that automate common tasks, like deployment or data processing. You can run these scripts to simplify repetitive work.

#### `deploy.py`

This repository contains `scripts/deploy.py`, a Python deployment script that uses [`fabric-cicd`](https://microsoft.github.io/fabric-cicd/).

#### `scripts/bpa/`

This folder contains configuration files for static analysis tools such as the [Tabular Editor Best Practice Analyzer](https://docs.tabulareditor.com/te2/Best-Practice-Analyzer-Improvements.html) and [Power BI Inspector (v2)](https://github.com/NatVanG/PBI-InspectorV2). These community tools enable automated testing of Power BI semantic models, reports, and other Microsoft Fabric artifacts against a set of shared best practice rules. By maintaining rule definitions and settings here, you can ensure consistent quality checks and enforce standards across your project using these tools in local development or CI/CD pipelines.

### `src/`

The main source folder for your Power BI/Fabric project. It contains all the project files, including reports, models, resources, and configuration files.

> [!NOTE]
> Most of your work will happen here.

| File/Folder              | Purpose                                                      |
|--------------------------|--------------------------------------------------------------|
| `Sales.Report/`          | Contains the Power BI report definition, visuals, and resources |
| `Sales.SemanticModel/`   | Contains the semantic model definition, tables, relationships, and metadata |
| `Sales.pbip`             | The main Power BI Project file referencing all artifacts      |
| `parameter.yml`          | Deployment parameters, used by `fabric-cicd` ([docs](https://microsoft.github.io/fabric-cicd/0.1.28/how_to/parameterization/)). The file is never explicitly referenced as it will be discovered in this location automatically. |

### `.gitignore`

This file tells Git which files or folders to ignore (not track). For example, temporary files, build outputs, or sensitive information should be listed here to avoid accidentally sharing them.

`.gitignore` files can be nested. For example, there is `src/.gitignore` with additional ignore rules for PBIP.

---

If you are new to Git or GitHub, don't worry! Each of these folders and files helps organize your project and automate tasks, making collaboration and deployment easier. For more details, check the documentation or ask your team for guidance.