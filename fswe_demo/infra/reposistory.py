from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from fswe_demo.domain.recommendation.exceptions import (
    PopularItemNotFoundError,
    PopularItemRepoError,
)
from fswe_demo.domain.recommendation.popular import ItemPopularity
from fswe_demo.domain.recommendation.reposistory import PopularItemRepository
from fswe_demo.infra.orm.models import PopularItem


class PopularItemSQLAlchemyRepository(PopularItemRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, product_asin: str) -> ItemPopularity:
        orm = self.session.get(PopularItem, product_asin)

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
            orms: list[PopularItem] = self.session.query(PopularItem).all()
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
