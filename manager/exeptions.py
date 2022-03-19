"""Models exception"""


class FieldException(Exception):
    """
    Raises when ``Field`` used with wrong logic
    """
    pass


class ModelDoesNotExists(Exception):
    """
    Raised when model does not exists
    """
    pass


class ModelOperationError(Exception):
    """
    Raised when model operation has wrong format
    """
    pass


class DatabaseNameError(Exception):
    """
    Raised on db name problems
    """
    pass


class QuerySetOperationError(Exception):
    """
    Raised when query set operation has wrong usage
    """
    pass
