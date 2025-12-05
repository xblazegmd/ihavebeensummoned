# Some nice error types that'll help throughout the application
# Base class for all errors in the application
class IHBSError(Exception):
    """
    Base class for all errors in the application
    """
    def __init__(self, *args):
        super().__init__(*args)

# In case _____ is not found
class NotFoundError(Exception):
    """
    In case _____ is not found
    """
    def __init__(self, *args):
        super().__init__(*args)

# The attempted operation failed to run
class OperationFailedError(Exception):
    """
    The attempted operation failed to run
    """
    def __init__(self, *args):
        super().__init__(*args)

# The attempted operation is on cooldown
class CooldownError(Exception):
    """
    The attempted operation is on cooldown
    """
    def __init__(self, *args, remaining: int):
        super().__init__(*args)
        self.remaining = remaining

# External API errors

# An unexpected error when connecting to the Boomlings endpoint
class BoomlingsError(IHBSError):
    """
    An unexpected error when connecting to the Boomlings endpoint
    """
    ...

# Request to the API returned a 403 FORBIDDEN error
class HTTPForbiddenError(IHBSError):
    """
    Request to the API returned a 403 FORBIDDEN error

    This usually happens when the request to the Boomlings endpoint is invalid (no www subdomain, non-empty User-Agent)
    """
    ...