from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from loguru import logger
from sqlalchemy.orm import Session

from fswe_demo.application.dto.mappers import fpgrowth_recommendation_to_rec_dto
from fswe_demo.application.dto.recs import (
    Recommendation,
    RecommendationsResponse,
)
from fswe_demo.domain.recommendation.exceptions import (
    FPGrowthRecommendationNotFoundError,
    FPGrowthRecommendationRepoError,
    PopularItemNotFoundError,
    PopularItemRepoError,
)
from fswe_demo.infra.db.get_conn import get_session
from fswe_demo.infra.reposistory import (
    FPGrowthRecommendationSQLAlchemyRepository,
    PopularItemSQLAlchemyRepository,
)

router = APIRouter(prefix="/recs", tags=["recommendations"])


@router.get("/popular")
def get_item_popularity(
    db_session: Annotated[Session, Depends(get_session)],
    count: int = Annotated[
        ...,
        Query(
            example=50,
            ge=1,
            le=100,
            description="Number of popular items to return",
        ),
    ],
) -> RecommendationsResponse:
    repo = PopularItemSQLAlchemyRepository(db_session)
    try:
        item_popularity_list = repo.get_all()
        recs = [
            Recommendation(
                product_asin=item.product_asin,
                probability=item.normalized_count,
            )
            for item in item_popularity_list
        ]
        popular_recs_response = RecommendationsResponse(recommendations=recs)
        popular_recs_response = popular_recs_response.get_recommendations(top_n=count)
    except PopularItemRepoError as e:
        # Map domain error to HTTP 500
        raise HTTPException(status_code=500, detail=str(e)) from e
    except PopularItemNotFoundError as e:
        logger.error("Popular items not found: %s", e)
        raise HTTPException(status_code=404, detail=str(e)) from e
    return popular_recs_response


@router.get("/fpgrowth")
def get_fp_growth_recs(
    db_session: Annotated[Session, Depends(get_session)],
    asin: str = Annotated[
        str,
        Query(
            example="B0BGNG1294",
            description="Amazon ASIN to fetch FP-Growth recommendations",
        ),
    ],
    count: int = Annotated[
        ...,
        Query(
            10,
            ge=1,
            le=50,
            description="Number of FP-Growth recommendations to return",
        ),
    ],
) -> RecommendationsResponse:
    """Fetch FP-Growth recommendations for a given ASIN.Falls back to popular items if no recs or on repo/DB errors."""
    fp_repo = FPGrowthRecommendationSQLAlchemyRepository(db_session)

    try:
        fp_resp = fp_repo.get(
            asin,
        )  # may raise repo errors; may also be None if you adopt that style

        recs = fpgrowth_recommendation_to_rec_dto(fp_resp)
        recs = recs.get_recommendations(top_n=count)

    except (
        FPGrowthRecommendationNotFoundError,
        FPGrowthRecommendationRepoError,
    ) as e:
        logger.warning(
            f"FP-Growth fallback to popular: asin={asin}, "
            f"error_type={e.__class__.__name__}, reason={e}",
        )

        # Rollback the failed transaction before proceeding with fallback
        db_session.rollback()
        popular_items_recs = get_item_popularity(db_session, count=count)
        return popular_items_recs

    else:
        return recs
