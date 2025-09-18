from fswe_demo.application.use_cases.ingest_raw_data import (  # noqa: INP001
    IngestRawDataUseCase,
)
from fswe_demo.infra.adapters.excel_reader import ExcelFileReader
from fswe_demo.infra.adapters.postgres_writer import PostgresWriter
from fswe_demo.infra.db.get_conn import get_db_connection
from fswe_demo.settings import settings


def ingest_raw_data_from_excel() -> None:
    db_connection = get_db_connection()
    reader = ExcelFileReader(file_path=settings.data_source_path)
    writer = PostgresWriter(connection=db_connection, table_name="ratings")
    IngestRawDataUseCase(reader, writer).execute()
