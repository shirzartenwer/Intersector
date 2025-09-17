from typing import List, TypeVar, Generic
import time
import random
from .models import IntersectionStrategy, IntersectionResult
from .exceptions import InvalidCollectionException, InvalidStrategyException, CollectionTooLargeException
from config import MAX_COLLECTION_SIZE, RANDOM_ELEMENT_MIN, RANDOM_ELEMENT_MAX, VALUE_RANGE_MULTIPLIER

T = TypeVar('T')


class CollectionGenerator:
    """Handles generation of test collections with controlled overlap."""
    
    @staticmethod
    def generate_with_overlap(size_a: int, size_b: int, overlap_ratio: float = 0.1) -> tuple[List[int], List[int]]:
        """Generate two collections with specified sizes and overlap ratio."""
        if size_a == 0 or size_b == 0:
            return (
                [random.randint(RANDOM_ELEMENT_MIN, RANDOM_ELEMENT_MAX) for _ in range(size_a)], 
                [random.randint(RANDOM_ELEMENT_MIN, RANDOM_ELEMENT_MAX) for _ in range(size_b)]
            )
        
        max_value = max(size_a, size_b) * VALUE_RANGE_MULTIPLIER
        overlap_size = int(min(size_a, size_b) * overlap_ratio)
        
        common_elements = random.sample(range(RANDOM_ELEMENT_MIN, max_value), min(overlap_size, max_value - 1))
        remaining_pool = [x for x in range(RANDOM_ELEMENT_MIN, max_value) if x not in common_elements]
        
        collection_a = common_elements[:] + random.sample(remaining_pool, size_a - len(common_elements))
        collection_b = common_elements[:] + random.sample(remaining_pool, size_b - len(common_elements))
        
        return collection_a[:size_a], collection_b[:size_b]


class TwoCollectionIntersector(Generic[T]):
    def __init__(self, collection_a: List[T], collection_b: List[T], max_collection_size: int = MAX_COLLECTION_SIZE):
        self._validate_inputs(collection_a, collection_b, max_collection_size)
        self.collection_a = collection_a
        self.collection_b = collection_b

    @classmethod
    def from_sizes(cls, size_a: int, size_b: int, overlap_ratio: float = 0.1, max_collection_size: int = MAX_COLLECTION_SIZE) -> "TwoCollectionIntersector[int]":
        collection_a, collection_b = CollectionGenerator.generate_with_overlap(size_a, size_b, overlap_ratio)
        return cls(collection_a, collection_b, max_collection_size)
        

    def intersect(self, strategy: IntersectionStrategy) -> IntersectionResult[T]:
        start_time = time.perf_counter()
        result = self._execute_intersection(strategy)
        execution_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds
        
        return IntersectionResult(
            intersection=result,
            execution_time_ms=execution_time,
            strategy_used=strategy,
            collection_sizes=(len(self.collection_a), len(self.collection_b))
        )
    
    def intersect_legacy(self, index: int) -> tuple[List[T], float]:
        """Legacy method for backward compatibility"""
        if index == 0:
            strategy = IntersectionStrategy.USE_FIRST_AS_HASHSET
        elif index == 1:
            strategy = IntersectionStrategy.USE_SECOND_AS_HASHSET
        else:
            raise InvalidStrategyException(f"Invalid index: {index}. Use 0 or 1.")
        
        result = self.intersect(strategy)
        return result.intersection, result.execution_time_ms / 1000  # Convert back to seconds
    
    
    def _execute_intersection(self, strategy: IntersectionStrategy) -> List[T]:
        if strategy == IntersectionStrategy.USE_FIRST_AS_HASHSET:
            hash_set = set(self.collection_a)
            iterator = self.collection_b
        elif strategy == IntersectionStrategy.USE_SECOND_AS_HASHSET:
            hash_set = set(self.collection_b)
            iterator = self.collection_a
        else:
            raise InvalidStrategyException(f"Unknown strategy: {strategy}")
        
        return [item for item in iterator if item in hash_set]
    
    @staticmethod
    def _validate_inputs(collection_a: List[T], collection_b: List[T], max_size: int) -> None:
        if collection_a is None or collection_b is None:
            raise InvalidCollectionException("Collections cannot be None")
        
        collections = [("collection_a", collection_a), ("collection_b", collection_b)]
        for name, collection in collections:
            if len(collection) > max_size:
                raise CollectionTooLargeException(len(collection), max_size)
    


