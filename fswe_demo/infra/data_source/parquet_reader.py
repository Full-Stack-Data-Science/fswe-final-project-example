import math

import pandas as pd
from tqdm import tqdm


class ParquetReader:
    """
    Parquet Data Source Reader for batch ingestion.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_ratings_parquet(self) -> pd.DataFrame:
        """Reads the Parquet file and returns a DataFrame."""
        try:
            rating_df = pd.read_parquet(self.file_path)
            return rating_df
        except Exception as e:
            raise RuntimeError(f"Failed to read Parquet file: {e}")

    def save_to_postgres(
        self, df: pd.DataFrame, table_name: str, connection, chunk_size: int = 10000,
    ) -> None:
        """
        Saves the DataFrame to a PostgreSQL table in chunks, showing a progress bar.
        """
        try:
            total_chunks = math.ceil(len(df) / chunk_size)
            # tqdm on the range of start indices
            for idx in tqdm(
                range(0, len(df), chunk_size),
                total=total_chunks,
                desc=f"Inserting into {table_name}",
                unit="chunk",
            ):
                chunk = df.iloc[idx : idx + chunk_size]
                chunk.to_sql(
                    table_name,
                    connection,
                    if_exists="append" if idx > 0 else "replace",
                    index=False,
                )
        except Exception as e:
            raise RuntimeError(f"Failed to save DataFrame to PostgreSQL in chunks: {e}")
