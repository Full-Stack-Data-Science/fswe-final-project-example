from fswe_demo.application.use_cases.ingest_raw_data import IngestRawDataUseCase


def ingest_raw_data():
    IngestRawDataUseCase().execute()
