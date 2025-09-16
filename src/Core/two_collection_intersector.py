from typing import List, Union
import time
import random


class TwoCollectionIntersector:
    collection_a: List[float]
    collection_b: List[float]
    runtime: float


    def __init__(self, collection_a: List[float], collection_b: List[float]):
        self.collection_a = collection_a
        self.collection_b = collection_b

    @classmethod
    def from_sizes(cls, size_a: int, size_b: int) -> "TwoCollectionIntersector":
        collection_a = [random.random() for _ in range(size_a)]
        collection_b = [random.random() for _ in range(size_b)]
        return cls(collection_a, collection_b)
        

    def intersect(self, index:int) -> Union[List[float], float]:
        result = []
        start_time = time.time()
        if index == 0:
            hash_set = set(self.collection_a)
            iterator = self.collection_b
        else:
            hash_set = set(self.collection_b)
            iterator = self.collection_a

        
        for item in iterator:
            if item in hash_set:
                result.append(item)

        self.runtime = time.time() - start_time
        return result, self.runtime


