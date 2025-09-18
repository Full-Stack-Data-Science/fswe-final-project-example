from fswe_demo.application.dto.recs import Recommendation, RecommendationsResponse
from fswe_demo.domain.recommendation.recs import (
    FPGrowthRecommendationsResponse,
)


def fpgrowth_recommendation_to_rec_dto(
    recommendation: FPGrowthRecommendationsResponse,
) -> RecommendationsResponse:
    recs = recommendation.recommendations

    dto_recommendations = [
        Recommendation(
            product_asin=rec.asin,
            probability=rec.confidence,
        )
        for rec in recs
    ]

    return RecommendationsResponse(recommendations=dto_recommendations)
