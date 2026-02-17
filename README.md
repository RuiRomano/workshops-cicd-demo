
## Requirements

- Python runtime 3.9 to 3.12 (3.13 is not supported)
- 

## Repository Structure

| File/Folder       | Purpose                                                      |
|-------------------|--------------------------------------------------------------|
| `.bpa/`           | Best practice analyzer configuration                         |
| `.devcontainer/`  | Dev Container setup for consistent development environments  |
| `.github/`        | GitHub Actions workflows and GitHub-specific files           |
| `.vscode/`        | VS Code settings and recommended extensions                  |
| `scripts/`        | Helper scripts for automation and deployment                 |
| `src/`            | Main Power BI project files and resources                    |
| `.gitignore`      | Specifies files/folders to be ignored by Git                 |

This repository is organized to help you manage your Power BI project efficiently, especially if you are new to Git, GitHub, and automation with GitHub Actions. Here is a quick guide to the main folders and files you will find:

### `.bpa/`

This folder contains configuration files for static analysis tools such as the [Tabular Editor Best Practice Analyzer](https://docs.tabulareditor.com/te2/Best-Practice-Analyzer-Improvements.html) and [Power BI Inspector (v2)](https://github.com/NatVanG/PBI-InspectorV2). These community tools enable automated testing of Power BI semantic models, reports, and other Microsoft Fabric artifacts against a set of shared best practice rules. By maintaining rule definitions and settings here, you can ensure consistent quality checks and enforce standards across your project using these tools in local development or CI/CD pipelines.

### `.devcontainer/`

Contains configuration files for [Dev Containers](https://containers.dev/), which allow you to develop inside a consistent, pre-configured environment. This is useful for onboarding and ensuring everyone uses the same tools and dependencies.

The provided devcontainer definition at `.devcontainer/devcontainer.json` is preconfigured with recommended vscode extensions as well as the [`fabric-cicd`](https://microsoft.github.io/fabric-cicd/) library and necessary runtimes.

A devcontainer environment can be launched locally with Docker installed, or in the cloud via [GitHub Codespaces](https://github.com/codespaces) - a repository opened in a GitHub Codespace can be edited either from vscode on your desktop or in the browser at <https://github.dev>.

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

This repository contains `scripts/deploy.py`, a Python deployment script that uses [`fabric-cicd`](https://microsoft.github.io/fabric-cicd/).

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