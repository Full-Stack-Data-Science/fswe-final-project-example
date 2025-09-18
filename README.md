# Setup and Development Guide

This project is a comprehensive data engineering and analytics platform. Follow this guide to set up your development environment and run the application.

## Prerequisites

Before you begin, ensure you have the following tools installed:

- **Conda**: Package manager and environment management system (Anaconda or Miniconda)
- **Python 3.11.9**: Programming language and runtime (will be installed via conda)
- **pip**: Python package installer (comes with conda environments)
- **Make**: Build automation tool for running common development tasks
- **Docker & Docker Compose**: For containerized infrastructure services
- **Git**: Version control system

## Tool Introductions

This project leverages several modern development tools to enhance productivity and maintainability:

### Conda - Package and Environment Manager
**Conda** is an open-source package management system and environment management system that runs on Windows, macOS, and Linux. Key features include:
- Cross-platform package management
- Environment isolation with specific Python versions
- Dependency resolution and conflict management
- Support for both Python and non-Python packages

### Poe the Poet - Task Runner
**Poe the Poet** (poethepoet) is a task runner and build tool for Python projects. It provides a simple, standardized way to define and run project tasks. Key features:
- Task definitions in `pyproject.toml`
- Cross-platform script execution
- Environment variable support
- Task dependencies and composition

### DBT - Data Build Tool
**DBT (Data Build Tool)** is a command-line tool that enables data analysts and engineers to transform data in their warehouse more effectively. It brings software engineering practices to analytics:
- SQL-based transformations
- Version control for data models
- Automated testing and documentation
- Dependency management for data pipelines

### Make - Build Automation
**Make** is a classic build automation tool that helps organize and execute common development tasks. In this project, it's used for:
- Infrastructure management commands
- Simplified Docker operations
- Consistent development workflows

## Getting Started

### 1. Environment Configuration

Copy the example environment file and configure your settings:

```sh
cp .env.example .env
```

Edit the `.env` file to match your local configuration. This file contains database credentials, API keys, and other environment-specific settings.

### 2. Environment Variables Setup

Export the environment variables to make them available in your current shell session:

```sh
export PROJ_DIR=$(pwd)
echo "Project directory set to $PROJ_DIR"
set -a && source .env && set +a
```

This command:
- `set -a`: Automatically exports all variables that are assigned
- `source .env`: Loads variables from the .env file
- `set +a`: Disables automatic export for subsequent assignments

### 3. Dependency Installation

Create a conda environment with Python 3.13 and install project dependencies:

```sh
conda create --prefix ./venv python=3.13
conda activate ./venv
pip install -r requirements.txt
pip install -e .
```

This will create an isolated conda environment with the specified Python version, install all required dependencies, and install the current package in editable mode.

**Note**: If you want to use the `poe` task runner commands, you'll also need to install poethepoet:

```sh
pip install poethepoet
```

### 4. Infrastructure Services

Start the required infrastructure services (PostgreSQL, etc.) using Docker Compose:

```sh
make infra-up
```

This command launches all containerized services defined in the docker-compose files.

### 5. Monitor Infrastructure

View real-time logs from all infrastructure services:

```sh
make infra-logs
```

Use this to troubleshoot any issues with the containerized services.

### 6. Data Ingestion Pipeline

Execute the raw data ingestion pipeline using **Poe the Poet** (a task runner for Python projects that provides a simple way to define and run project tasks):

```sh
poe ingest-raw-data
```

**Poe the Poet** reads task definitions from `pyproject.toml` and provides a consistent interface for running complex commands.

### 7. DBT Profile Configuration

**DBT (Data Build Tool)** is used for data transformation and analytics engineering. Set up the DBT profile by creating a `profiles.yml` file:

```sh
(
cd fswe_demo/infra/dbt/ecommerce &&
cat <<EOF > profiles.yml
ecommerce:
  outputs:
    dev:
      dbname: $POSTGRES_DB
      host: $POSTGRES_HOST
      pass: $POSTGRES_PASSWORD
      port: $POSTGRES_PORT
      schema: public
      threads: 1
      type: postgres
      user: $POSTGRES_USER
  target: dev
EOF
)
```

This configuration tells DBT how to connect to your PostgreSQL database for data transformations.
> Tips: Follow [best practices](https://docs.getdbt.com/best-practices) on how to structure and write DBT projects.

After that, check the DBT connection:

```sh
(cd fswe_demo/infra/dbt/ecommerce && dbt debug --profiles-dir .)
```
If `All checks passed!` is shown, the connection is successful.

Then, install DBT dependencies:

```sh
(cd fswe_demo/infra/dbt/ecommerce && dbt deps --profiles-dir .)
```

### 8. Build DBT Models

```sh
(cd fswe_demo/infra/dbt/ecommerce && dbt build --select staging.ecommerce+ intermediate.product_affinity+ mart+ --profiles-dir .)
```

This command will execute the DBT models defined in your project.

### 9 (Optional). View DBT Documentation
Generate and serve DBT documentation to explore your data models:

```sh
(cd fswe_demo/infra/dbt/ecommerce && dbt docs generate --profiles-dir .)
(cd fswe_demo/infra/dbt/ecommerce && dbt docs serve --profiles-dir . --port 8051)
```

Visit `http://localhost:8051` in your web browser to view the documentation.


### 11. Run the notebook ``002_fp_growth.ipynb`` to generate FP-Growth recommendations and store them in the database.

### 10. Run the Application
Start the FastAPI application:

```sh
uvicorn fswe_demo.main:app --host 0.0.0.0 --port 8000
```

### 11. Run the notebook ``002_fp_growth.ipynb`` to generate FP-Growth recommendations and store them in the database.