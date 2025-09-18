from pydantic import BaseModel, Field


class PopularRecommendation(BaseModel):
    product_asin: str = Field(..., description="The ASIN of the product")
    probability: float = Field(
        ...,
        description="The probability score for recommendation",
    )


class PopularRecommendationsResponse(BaseModel):
    recommendations: list[PopularRecommendation] = Field(
        ...,
        description="List of popular product recommendations",
    )

    # Define business logic methods
    def get_recommendations(self, top_n: int = 10) -> "PopularRecommendationsResponse":
        """Get top N popular recommendations."""
        recommendations = self.recommendations[:top_n]
        return PopularRecommendationsResponse(recommendations=recommendations)


class ItemPopularityResponse(BaseModel):
    product_asin: str = Field(..., description="The ASIN of the product")
    count: int | None = Field(None, description="The number of ratings for the product")
