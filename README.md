# How to guide

1. Copy `.env.example` to `.env` and update the environment variables as needed.

2. Install the required dependencies using:
    ```
    uv sync --all-groups
    ```

2. Run `make infra-up` to start the infrastructure services.

3. Run `make infra-logs` to view the logs of the infrastructure services.

4. Run `uv run poe ingest-raw-data` to execute the raw data ingestion pipeline.