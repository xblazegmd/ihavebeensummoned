# Some nice error types that'll help throughout the application
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