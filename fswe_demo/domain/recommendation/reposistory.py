from abc import ABC, abstractmethod

from fswe_demo.domain.recommendation.popular import ItemPopularity


class PopularItemRepository(ABC):
    @abstractmethod
    def get(self, product_asin: str) -> ItemPopularity: ...
    @abstractmethod
    def get_all(self) -> list[ItemPopularity]: ...
