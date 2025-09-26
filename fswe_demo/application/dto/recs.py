from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    product_asin: str = Field(..., description="The ASIN of the product")
    probability: float = Field(
        ...,
        description="The probability score for recommendation",
    )


class RecommendationsResponse(BaseModel):
    recommendations: list[Recommendation] = Field(
        ...,
        description="List of popular product recommendations",
    )

    # Define business logic methods
    def get_recommendations(self, top_n: int = 10) -> "RecommendationsResponse":
        """Get top N popular recommendations."""
        recommendations = self.recommendations[:top_n]
        return RecommendationsResponse(recommendations=recommendations)


class ItemPopularityResponse(BaseModel):
    product_asin: str = Field(..., description="The ASIN of the product")
    count: int | None = Field(None, description="The number of ratings for the product")
