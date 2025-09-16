class ParquetReaderError(Exception):
    """Custom exception for errors encountered while reading Parquet files."""


class PostgresWriteError(Exception):
    """Custom exception for errors encountered while writing to PostgreSQL."""
