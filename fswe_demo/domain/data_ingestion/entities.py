"""
Domain model for data ingestion.

Represents the core entities and value objects for raw data ingestion.
"""

from typing import Annotated

from pydantic import BaseModel


class LocalRawFile(BaseModel):
    """Represents raw rating data ingested from a data source."""

    source_path: Annotated[str, "Path to the local raw data file."]
    file_type: Annotated[str, "Type of the file, e.g., 'parquet', 'csv'."]
    ingestion_date: Annotated[str, "Date when the data was ingested."]
    record_count: Annotated[int, "Number of records in the raw data file."] = None
