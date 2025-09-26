from pydantic import BaseModel, Field, model_validator


class ItemPopularity(BaseModel):
    product_asin: str = Field(..., description="The ASIN of the product")
    count: int | None = Field(None, description="The number of ratings for the product")
    normalized_count: float | None = Field(
        None,
        description="The normalized count of ratings for the product",
    )
    is_popular: bool = Field(..., description="Whether the product is popular")

    @model_validator(mode="after")
    def check_count_if_popular(self) -> "ItemPopularity":
        if self.is_popular and self.count is None and self.normalized_count is None:
            error_msg = "`count` and `normalized_count` must be defined when `is_popular` is True"
            raise ValueError(error_msg)
        return self
