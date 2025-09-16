from loguru import logger

from fswe_demo.domain.data_ingestion.ports import BulkReadPort, BulkWritePort
from fswe_demo.settings import settings


class IngestRawDataUseCase:
    """Use case for ingesting raw data from a Parquet file to PostgreSQL."""

    def __init__(self, reader: BulkReadPort, writer: BulkWritePort) -> None:
        self.reader = reader
        self.writer = writer

    def execute(self) -> None:
        """Executes the data ingestion process."""
        data_path = settings.data_source_path

        rating_df = self.reader.read()
        source_metadata = self.reader.build_entity()
        logger.info(f"Read {len(rating_df)} records from {data_path}.")
        logger.info(f"Stats: {source_metadata.model_dump_json()}")

        self.writer.write(rating_df)
        logger.info(f"Ingested {len(rating_df)} records from {data_path}.")
