# Setup and Development Guide

This project is a comprehensive data engineering and analytics platform. Follow this guide to set up your development environment and run the application.

## Prerequisites

Before you begin, ensure you have the following tools installed:

- **uv**: A fast Python package and project manager written in Rust. It's used as a drop-in replacement for pip and pip-tools with significantly faster dependency resolution and installation.
- **Make**: Build automation tool for running common development tasks
- **Docker & Docker Compose**: For containerized infrastructure services
- **Git**: Version control system

## Tool Introductions

This project leverages several modern development tools to enhance productivity and maintainability:

### uv - Modern Python Package Manager
**uv** is a fast Python package and project manager written in Rust. It serves as a drop-in replacement for pip and pip-tools with significantly faster dependency resolution and installation. Key benefits include:
- 10-100x faster than traditional pip
- Built-in virtual environment management
- Unified dependency resolution
- Cross-platform compatibility

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

Install project dependencies using **uv**, which provides faster and more reliable dependency management compared to traditional pip:

```sh
uv sync --all-groups
```

The `--all-groups` flag ensures all optional dependency groups (development, testing, etc.) are installed.

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
uv run poe ingest-raw-data
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
(cd fswe_demo/infra/dbt/ecommerce && uv run dbt debug --profiles-dir .)
```
If `All checks passed!` is shown, the connection is successful.

Then, install DBT dependencies:

```sh
(cd fswe_demo/infra/dbt/ecommerce && uv run dbt deps --profiles-dir .)
```

### 8. Build DBT Models

```sh
(cd fswe_demo/infra/dbt/ecommerce && uv run dbt build --select staging.ecommerce+ intermediate.product_affinity+ --profiles-dir .)
```

This command will execute the DBT models defined in your project.

### 9 (Optional). View DBT Documentation
Generate and serve DBT documentation to explore your data models:

```sh
(cd fswe_demo/infra/dbt/ecommerce && uv run dbt docs generate --profiles-dir .)
(cd fswe_demo/infra/dbt/ecommerce && uv run dbt docs serve --profiles-dir . --port 8051)
```

Visit `http://localhost:8051` in your web browser to view the documentation.