from pydantic import BaseModel, Field


class FPGrowthRecommendation(BaseModel):
    asin: str = Field(
        ...,
        description="The ASIN of the recommended product",
        alias="recommendation",
    )
    confidence: float


class FPGrowthRecommendationsResponse(BaseModel):
    product_asin: str = Field(..., description="The ASIN of the target product")
    recommendations: list[FPGrowthRecommendation] = Field(
        ...,
        description="List of recommended products",
    )
