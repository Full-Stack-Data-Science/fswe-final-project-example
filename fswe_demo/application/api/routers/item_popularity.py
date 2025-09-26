from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from fswe_demo.application.dto.recs import ItemPopularityResponse
from fswe_demo.domain.recommendation.exceptions import PopularItemNotFoundError
from fswe_demo.infra.db.get_conn import get_session
from fswe_demo.infra.reposistory import PopularItemSQLAlchemyRepository

router = APIRouter(prefix="/item_popularity", tags=["recommendations"])


@router.get(
    "/item_popularity",
    response_model=ItemPopularityResponse,
)
def get_item_popularity(
    product_asin: Annotated[
        str,
        Query(
            ...,
            description="Amazon ASIN (10 uppercase letters/digits)",
            example="B01K8B8YA8",
        ),
    ],
    db_session: Annotated[Session, Depends(get_session)],
) -> dict:
    repo = PopularItemSQLAlchemyRepository(db_session)
    try:
        item_popularity = repo.get(product_asin)
        item_popularity_response = ItemPopularityResponse(
            product_asin=item_popularity.product_asin,
            count=item_popularity.count,
        )
    except PopularItemNotFoundError as e:
        # Map domain error to HTTP 404
        raise HTTPException(status_code=404, detail=str(e)) from e
    return item_popularity_response
