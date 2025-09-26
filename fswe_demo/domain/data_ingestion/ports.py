from abc import ABC, abstractmethod
from typing import Protocol

from fswe_demo.domain.data_ingestion.entities import LocalRawFile


class Tabular(Protocol):
    """A minimal, generic tabular handle. Spark DataFrame, Pandas DF, or Arrow Table can satisfy this."""


class BulkReadPort(ABC):
    """Port for bulk reading raw data from a data source."""

    @abstractmethod
    def read(self) -> Tabular:
        """Reads raw data from the data source and returns it in a tabular format."""
        ...

    @abstractmethod
    def build_entity(self) -> LocalRawFile:
        """Builds and returns an entity representing the raw data source."""
        ...


class BulkWritePort(ABC):
    """Port for bulk writing processed data to a destination."""

    @abstractmethod
    def write(self, data: Tabular) -> None:
        """Writes the processed data to the destination."""
        ...
