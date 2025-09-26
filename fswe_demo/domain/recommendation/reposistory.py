from abc import ABC, abstractmethod

from fswe_demo.domain.recommendation.popular_item import ItemPopularity
from fswe_demo.domain.recommendation.recs import FPGrowthRecommendationsResponse


class PopularItemRepository(ABC):
    @abstractmethod
    def get(self, product_asin: str) -> ItemPopularity: ...
    @abstractmethod
    def get_all(self) -> list[ItemPopularity]: ...


class FPGrowthRecommendationRepository(ABC):
    @abstractmethod
    def get(self, product_asin: str) -> FPGrowthRecommendationsResponse: ...
