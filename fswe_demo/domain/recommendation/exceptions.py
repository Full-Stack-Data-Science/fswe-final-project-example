class PopularItemNotFoundError(Exception):
    """Exception raised when a popular item is not found in the repository."""


class PopularItemRepoError(Exception):
    """Exception raised for errors in the popular item repository."""


class FPGrowthRecommendationRepoError(Exception):
    """Exception raised for errors in the FP-Growth recommendation repository."""


class FPGrowthRecommendationNotFoundError(Exception):
    """Exception raised when FP-Growth recommendations are not found in the repository."""
