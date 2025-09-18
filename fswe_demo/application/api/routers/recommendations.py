from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from fswe_demo.application.dto.recs import (
    PopularRecommendation,
    PopularRecommendationsResponse,
)
from fswe_demo.domain.recommendation.exceptions import PopularItemRepoError
from fswe_demo.infra.db.get_conn import get_session
from fswe_demo.infra.reposistory import PopularItemSQLAlchemyRepository

router = APIRouter(prefix="/recs", tags=["recommendations"])


@router.get("/popular", response_model=PopularRecommendationsResponse)
def get_item_popularity(
    db_session: Annotated[Session, Depends(get_session)],
    count: int = Annotated[
        ...,
        Query(
            example=50, ge=1, le=100, description="Number of popular items to return"
        ),
    ],
) -> dict:
    repo = PopularItemSQLAlchemyRepository(db_session)
    try:
        item_popularity_list = repo.get_all()
        recs = [
            PopularRecommendation(
                product_asin=item.product_asin,
                probability=item.normalized_count,
            )
            for item in item_popularity_list
        ]
        popular_recs_response = PopularRecommendationsResponse(recommendations=recs)
        popular_recs_response = popular_recs_response.get_recommendations(top_n=count)
    except PopularItemRepoError as e:
        # Map domain error to HTTP 500
        raise HTTPException(status_code=500, detail=str(e)) from e
    return popular_recs_response
