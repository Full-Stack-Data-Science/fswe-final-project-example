class PopularItemNotFoundError(Exception):
    """Exception raised when a popular item is not found in the repository."""


class PopularItemRepoError(Exception):
    """Exception raised for errors in the popular item repository."""
