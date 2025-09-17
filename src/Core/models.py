from dataclasses import dataclass
from enum import Enum
from typing import List, TypeVar, Generic

T = TypeVar('T')


class IntersectionStrategy(Enum):
    USE_FIRST_AS_HASHSET = 0
    USE_SECOND_AS_HASHSET = 1


@dataclass
class IntersectionResult(Generic[T]):
    intersection: List[T]
    execution_time_ms: float
    strategy_used: IntersectionStrategy
    collection_sizes: tuple[int, int]
    
    @property
    def intersection_size(self) -> int:
        return len(self.intersection)
    
    @property
    def efficiency_ratio(self) -> float:
        total_elements = sum(self.collection_sizes)
        return self.intersection_size / total_elements if total_elements > 0 else 0.01


