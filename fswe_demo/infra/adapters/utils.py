from pathlib import Path

import pandas as pd
from loguru import logger


def parquet_to_excel(parquet_path: str, excel_path: str) -> None:
    """
    Convert a single Parquet file to a single-sheet Excel file.

    Args:
        parquet_path: Path to the input Parquet file.
        excel_path: Path to the output Excel file.

    """
    parquet_file = Path(parquet_path)
    if not parquet_file.exists():
        msg = f"Parquet file not found: {parquet_file}"
        raise FileNotFoundError(msg)

    # Read the parquet file
    pandas_df = pd.read_parquet(parquet_file)

    # Write to Excel, single sheet named "Sheet1"
    pandas_df.to_excel(excel_path, sheet_name="Sheet1", index=False)

    logger.info(f"Saved Excel to {excel_path}")


# Example usage:
# parquet_to_excel("data/input.parquet", "data/output.xlsx")
