import json

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fswe_demo.domain.recommendation.exceptions import (
    FPGrowthRecommendationNotFoundError,
    FPGrowthRecommendationRepoError,
    PopularItemNotFoundError,
    PopularItemRepoError,
)
from fswe_demo.domain.recommendation.popular_item import ItemPopularity
from fswe_demo.domain.recommendation.recs import (
    FPGrowthRecommendationsResponse,
)
from fswe_demo.domain.recommendation.reposistory import (
    FPGrowthRecommendationRepository,
    PopularItemRepository,
)
from fswe_demo.infra.orm.models import FPGrowthRecommendationTable, PopularItemTable


class PopularItemSQLAlchemyRepository(PopularItemRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, product_asin: str) -> ItemPopularity:
        orm = self.session.get(PopularItemTable, product_asin)

        if not orm:
            msg = f"PopularItem with ASIN {product_asin} not found"
            raise PopularItemNotFoundError(msg)
        return ItemPopularity(
            product_asin=orm.product_asin,
            count=orm.size,
            normalized_count=orm.prob,
            is_popular=True,
        )

    def get_all(self) -> list[ItemPopularity]:
        try:
            orms: list[PopularItemTable] = self.session.query(PopularItemTable).all()
        except SQLAlchemyError as e:
            msg = f"Error fetching popular items: {e}"
            raise PopularItemRepoError(msg) from e

        if not orms:
            msg = "No popular items found"
            raise PopularItemNotFoundError(msg)

        return [
            ItemPopularity(
                product_asin=orm.product_asin,
                count=orm.size,
                normalized_count=orm.prob,
                is_popular=True,
            )
            for orm in orms
        ]


class FPGrowthRecommendationSQLAlchemyRepository(FPGrowthRecommendationRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, product_asin: str) -> FPGrowthRecommendationsResponse:
        try:
            orm = self.session.get(
                FPGrowthRecommendationTable,
                product_asin,
            )
        except SQLAlchemyError as e:
            msg = (
                f"Error fetching FP-Growth recommendations for ASIN {product_asin}: {e}"
            )
            raise FPGrowthRecommendationRepoError(msg) from e

        if not orm:
            msg = f"No FP-Growth recommendations found for ASIN {product_asin}"
            raise FPGrowthRecommendationNotFoundError(msg)

        # Get results and parse JSON strings
        target_asin = orm.product_asin
        # Dont need to load from json string as sqlalchemy JSONB type auto converts
        recommendations = orm.recommendations

        recommendation_response = FPGrowthRecommendationsResponse(
            product_asin=target_asin,
            recommendations=recommendations,
        )
        return recommendation_response
