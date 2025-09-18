import click

from fswe_demo.infra.adapters.utils import parquet_to_excel


@click.command()
@click.option(
    "--input-file",
    type=click.Path(exists=True),
    required=True,
    help="Path to the input Parquet file",
)
@click.option(
    "--output-file",
    type=click.Path(),
    required=True,
    help="Path to the output Excel file",
)
def convert_parquet_to_excel(input_file: str, output_file: str) -> None:
    """Convert a Parquet file to an Excel file."""
    parquet_to_excel(input_file, output_file)


if __name__ == "__main__":
    convert_parquet_to_excel()

# Example usage:
# uv run python tools/convert_parquet_to_excel.py --input-file data/rating_sample.parquet --output-file data/rating_sample.xlsx
