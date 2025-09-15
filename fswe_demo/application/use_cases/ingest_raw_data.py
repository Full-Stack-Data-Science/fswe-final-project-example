from loguru import logger
from sqlalchemy import create_engine

from fswe_demo.infra.data_source.parquet_reader import ParquetReader
from fswe_demo.settings import settings


class IngestRawDataUseCase:
    """
    Use case for ingesting raw data from a Parquet file to PostgreSQL.
    """

    def __init__(self):
        self.parquet_reader = ParquetReader(file_path=settings.data_source_path)
        self.db_connection = create_engine(
            f"postgresql+psycopg2://{settings.postgres_user}:{settings.postgres_password.get_secret_value()}@"
            f"{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}",
        )

    def execute(self) -> None:
        """
        Executes the data ingestion process.
        """
        data_path = settings.data_source_path

        rating_df = self.parquet_reader.read_ratings_parquet()
        self.parquet_reader.save_to_postgres(rating_df, "ratings", self.db_connection)
        logger.info("Data ingestion completed successfully.")
        logger.debug(f"Ingested {len(rating_df)} records from {data_path}.")
