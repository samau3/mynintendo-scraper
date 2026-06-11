class DatabaseError(Exception):
    """Custom exception for database-related errors."""

    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception


class CSSTagSelectorError(Exception):
    """Custom exception for database-related errors."""

    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception


class IncompleteScrapeError(Exception):
    """Raised when scraping cannot load the full rewards list."""

    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception


class CustomError(Exception):
    def __init__(self, message, original_exception=None):
        super().__init__(message)
        self.original_exception = original_exception
