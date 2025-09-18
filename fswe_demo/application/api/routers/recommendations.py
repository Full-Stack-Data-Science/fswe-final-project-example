import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from fswe_demo.application.dto.recs import (
    Recommendation,
    RecommendationsResponse,
)
from fswe_demo.domain.recommendation.exceptions import PopularItemRepoError
from fswe_demo.infra.db.get_conn import get_session
from fswe_demo.infra.reposistory import PopularItemSQLAlchemyRepository

router = APIRouter(prefix="/recs", tags=["recommendations"])


@router.get("/popular", response_model=RecommendationsResponse)
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
) -> dict:
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
    return popular_recs_response


@router.get("/fpgrowth", response_model=RecommendationsResponse)
def get_fp_growth_recs(
    db_session: Annotated[Session, Depends(get_session)],
    asin: Annotated[
        str,
        Query(
            example="B0BGNG1294",
            description="Amazon ASIN to fetch FP-Growth recommendations",
        ),
    ],
    fallback_count: Annotated[
        int,
        Query(
            example=10,
            ge=1,
            le=50,
            description="Number of popular items to return if no FP-Growth recs found",
        ),
    ],
) -> dict:
    """
    Fetch FP-Growth recommendations for a given ASIN.

    - Reads raw JSON string from DB
    - Parses to list of Recommendation objects
    - Falls back to popular items if no recs
    """
    # 1️Try to fetch FP-Growth recommendations
    sql = text(
        "SELECT recommendations FROM fpgrowth_product_recommendations "
        "WHERE product_asin = :asin",
    )
    row = db_session.execute(sql, {"asin": asin}).fetchone()

    if row and row[0]:
        try:
            raw_val = row[0]
            parsed = json.loads(raw_val)
            if isinstance(parsed, str):  # handle double-encoded JSON
                parsed = json.loads(parsed)

            recs = [
                Recommendation(
                    product_asin=item["recommendation"][0],
                    probability=item.get("confidence", 0.0),
                )
                for item in parsed
            ]
            return RecommendationsResponse(recommendations=recs)

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Parse error: {e}") from e

    # 2️Fallback to popular items if no FP-Growth data
    popular_sql = text(
        "SELECT product_asin, prob FROM popular_items ORDER BY prob DESC LIMIT :n",
    )
    popular_rows = db_session.execute(popular_sql, {"n": fallback_count}).fetchall()
    fallback_recs = [
        Recommendation(product_asin=p_asin, probability=prob)
        for p_asin, prob in popular_rows
    ]
    return RecommendationsResponse(recommendations=fallback_recs)
