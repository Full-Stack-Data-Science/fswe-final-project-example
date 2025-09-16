import math

import pandas as pd
from sqlalchemy.engine.base import Engine
from tqdm import tqdm

from fswe_demo.domain.data_ingestion.exceptions import PostgresWriteError
from fswe_demo.domain.data_ingestion.ports import BulkWritePort


class PostgresWriter(BulkWritePort):
    def __init__(self, connection: Engine, table_name: str, **kwargs: int) -> None:
        self.connection = connection
        self.table_name = table_name
        self.chunk_size = kwargs.get("chunk_size", 10000)

    def write(self, data: pd.DataFrame) -> None:
        """Writes the DataFrame to a PostgreSQL table in chunks."""
        try:
            total_chunks = math.ceil(len(data) / self.chunk_size)
            # tqdm on the range of start indices
            for idx in tqdm(
                range(0, len(data), self.chunk_size),
                total=total_chunks,
                desc=f"Inserting into {self.table_name}",
                unit="chunk",
            ):
                chunk = data.iloc[idx : idx + self.chunk_size]
                chunk.to_sql(
                    self.table_name,
                    self.connection,
                    if_exists="append" if idx > 0 else "replace",
                    index=False,
                )
        except Exception as e:
            raise PostgresWriteError(self.table_name, e) from e
