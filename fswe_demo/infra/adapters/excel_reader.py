from datetime import UTC, datetime

import pandas as pd

from fswe_demo.domain.data_ingestion.entities import LocalRawFile
from fswe_demo.domain.data_ingestion.exceptions import ExcelReaderError
from fswe_demo.domain.data_ingestion.ports import BulkReadPort


class ExcelFileReader(BulkReadPort):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def read(self) -> pd.DataFrame:
        """Reads raw data from the Excel file and returns it as a Pandas DataFrame."""
        try:
            raw_df = pd.read_excel(self.file_path)
        except Exception as e:
            raise ExcelReaderError(self.file_path, e) from e
        else:
            self.raw_df = raw_df
            return raw_df

    def build_entity(self) -> LocalRawFile:
        """Builds a LocalRawFile entity from the Excel file metadata."""
        if not hasattr(self, "raw_df"):
            msg = "DataFrame not loaded. Call read() before building entity."
            raise ValueError(
                msg,
            )

        record_count = len(self.raw_df)

        return LocalRawFile(
            source_path=self.file_path,
            file_type="excel",
            ingestion_date=datetime.now(tz=UTC).isoformat(),
            record_count=record_count,
        )
