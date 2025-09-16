from datetime import UTC, datetime

import pandas as pd

from fswe_demo.domain.data_ingestion.entities import LocalRawFile
from fswe_demo.domain.data_ingestion.exceptions import ParquetReaderError
from fswe_demo.domain.data_ingestion.ports import BulkReadPort


class ParquetFileReader(BulkReadPort):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> pd.DataFrame:
        """Reads raw data from the Parquet file and returns it as a Pandas DataFrame."""
        try:
            raw_df = pd.read_parquet(self.file_path)
        except Exception as e:
            raise ParquetReaderError(self.file_path, e) from e
        else:
            self.raw_df = raw_df
            return raw_df

    def build_entity(self) -> LocalRawFile:
        """Builds a LocalRawFile entity from the Parquet file metadata."""
        if not hasattr(self, "raw_df"):
            msg = "DataFrame not loaded. Call read() before building entity."
            raise ValueError(
                msg,
            )

        record_count = len(self.raw_df)

        return LocalRawFile(
            source_path=self.file_path,
            file_type="parquet",
            ingestion_date=datetime.now(tz=UTC).isoformat(),
            record_count=record_count,
        )
