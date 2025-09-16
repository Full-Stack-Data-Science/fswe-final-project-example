import click  # noqa: INP001

TASKS = {
    "ingest_raw_data": "pipelines.ingest_raw:ingest_raw_data_from_parquet",
    # future_task: "module:function",
}


@click.command()
@click.option(
    "--task",
    type=click.Choice(TASKS.keys()),
    required=True,
    help="Task to run",
)
def main(task: str) -> None:
    module_name, func_name = TASKS[task].split(":")
    module = __import__(module_name, fromlist=[func_name])
    getattr(module, func_name)()


if __name__ == "__main__":
    main()
