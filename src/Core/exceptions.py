from config import MAX_COLLECTION_SIZE

class IntersectorException(Exception):
    """Base exception for intersector operations"""
    pass


class InvalidCollectionException(IntersectorException):
    """Raised when collection inputs are invalid"""
    pass


class InvalidStrategyException(IntersectorException):
    """Raised when an invalid intersection strategy is provided"""
    pass


class CollectionTooLargeException(IntersectorException):
    """Raised when collections exceed maximum allowed size for efficient processing"""
    
    def __init__(self, size: int, max_size: int = MAX_COLLECTION_SIZE):
        super().__init__(f"Collection size {size} exceeds maximum allowed size {max_size}")
        self.size = size
        self.max_size = max_size