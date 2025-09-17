from Core.two_collection_intersector import TwoCollectionIntersector
from Core.models import IntersectionStrategy, IntersectionResult
from Core.exceptions import InvalidCollectionException, InvalidStrategyException, CollectionTooLargeException
import pytest


@pytest.mark.parametrize("size_a, size_b", [(100, 200), (0, 0), (1, 1), (50, 50)])
def test_initialization(size_a, size_b):
    intersector = TwoCollectionIntersector.from_sizes(size_a, size_b)
    assert len(intersector.collection_a) == size_a
    assert len(intersector.collection_b) == size_b


def test_output_number_type(size_a=100, size_b=200):
    intersector = TwoCollectionIntersector.from_sizes(size_a, size_b)
    result = intersector.intersect(IntersectionStrategy.USE_FIRST_AS_HASHSET)
    assert isinstance(result, IntersectionResult)
    assert isinstance(result.intersection, list)
    assert all(isinstance(x, int) for x in result.intersection)
    assert isinstance(result.execution_time_ms, float)
    assert isinstance(result.strategy_used, IntersectionStrategy)
    assert isinstance(result.collection_sizes, tuple)

    
@pytest.mark.parametrize("size_a, size_b, strategy, expected_length", 
                          [(0, 100, IntersectionStrategy.USE_FIRST_AS_HASHSET, 0), 
                           (100, 0, IntersectionStrategy.USE_SECOND_AS_HASHSET, 0), 
                           (0, 0, IntersectionStrategy.USE_FIRST_AS_HASHSET, 0)])
def test_intersect_empty_collections(size_a, size_b, strategy, expected_length):
    intersector = TwoCollectionIntersector.from_sizes(size_a, size_b)
    result = intersector.intersect(strategy)
    assert result.intersection_size == expected_length
    assert result.execution_time_ms >= 0.0


@pytest.mark.parametrize("collection_a, collection_b, strategy, expected_length", 
                          [([1, 2, 3], [4, 5, 6], IntersectionStrategy.USE_FIRST_AS_HASHSET, 0),
                           ([1, 2, 3], [4, 5, 6], IntersectionStrategy.USE_SECOND_AS_HASHSET, 0)])
        
def test_intersect_no_common_elements(collection_a, collection_b, strategy, expected_length):
    intersector = TwoCollectionIntersector(collection_a, collection_b)
    result = intersector.intersect(strategy)
    assert result.intersection_size == expected_length
    assert result.execution_time_ms >= 0.0


@pytest.mark.parametrize("collection_a, collection_b, strategy, expected_length", 
                          [([1, 2, 3], [3, 5, 6], IntersectionStrategy.USE_FIRST_AS_HASHSET, 1),
                           ([1, 2, 3], [3, 5, 6], IntersectionStrategy.USE_SECOND_AS_HASHSET, 1),
                           ([1, 2, 4], [1, 2, 3], IntersectionStrategy.USE_FIRST_AS_HASHSET, 2),
                           ([1, 2, 4], [1, 2, 3], IntersectionStrategy.USE_SECOND_AS_HASHSET, 2)])
        
def test_intersect_some_common_elements(collection_a, collection_b, strategy, expected_length):
    intersector = TwoCollectionIntersector(collection_a, collection_b)
    result = intersector.intersect(strategy)
    assert result.intersection_size == expected_length
    assert result.execution_time_ms >= 0.0
    assert set(result.intersection) == set([x for x in collection_a if x in collection_b])


def test_strategy_consistency():
    """Test that different strategies produce identical results"""
    collection_a, collection_b = [1, 2, 3, 4], [3, 4, 5, 6]
    intersector = TwoCollectionIntersector(collection_a, collection_b)
    
    result1 = intersector.intersect(IntersectionStrategy.USE_FIRST_AS_HASHSET)
    result2 = intersector.intersect(IntersectionStrategy.USE_SECOND_AS_HASHSET)
    
    assert set(result1.intersection) == set(result2.intersection)
    assert result1.intersection_size == result2.intersection_size



def test_legacy_method_compatibility():
    """Test that legacy intersect method still works"""
    intersector = TwoCollectionIntersector([1, 2, 3], [2, 3, 4])
    result, runtime = intersector.intersect_legacy(0)
    assert isinstance(result, list)
    assert isinstance(runtime, float)
    assert set(result) == {2, 3}


def test_input_validation():
    """Test proper input validation"""
    with pytest.raises(InvalidCollectionException):
        TwoCollectionIntersector(None, [1, 2, 3])
    
    with pytest.raises(InvalidCollectionException):
        TwoCollectionIntersector([1, 2, 3], None)


def test_collection_too_large():
    """Test handling of oversized collections"""
    with pytest.raises(CollectionTooLargeException):
        large_collection = list(range(10_000_001))
        TwoCollectionIntersector(large_collection, [1, 2, 3])


def test_intersection_result_properties():
    """Test IntersectionResult computed properties"""
    intersector = TwoCollectionIntersector([1, 2, 3, 4], [3, 4, 5, 6])
    result = intersector.intersect(IntersectionStrategy.USE_FIRST_AS_HASHSET)
    
    assert result.intersection_size == 2  # [3, 4]
    assert result.collection_sizes == (4, 4)
    assert result.efficiency_ratio == 2/8  # 2 intersections out of 8 total elements


def test_efficiency_ratio_edge_cases():
    """Test efficiency_ratio with edge cases"""
    from Core.models import IntersectionResult
    
    # Test with total_elements = 0
    result_empty = IntersectionResult([], 0.0, IntersectionStrategy.USE_FIRST_AS_HASHSET, (0, 0))
    assert result_empty.efficiency_ratio == 0.01


def test_legacy_method_invalid_index():
    """Test legacy method with invalid index"""
    intersector = TwoCollectionIntersector([1, 2, 3], [2, 3, 4])
    
    with pytest.raises(InvalidStrategyException):
        intersector.intersect_legacy(2)


def test_execute_intersection_unknown_strategy():
    """Test _execute_intersection with invalid strategy"""
    intersector = TwoCollectionIntersector([1, 2, 3], [2, 3, 4])
    
    # Create an invalid strategy by using an enum value that doesn't exist
    # We need to mock this since we can't create invalid enum values directly
    with pytest.raises(InvalidStrategyException):
        intersector._execute_intersection(999)  # Invalid strategy value


def test_collection_too_large_validation():
    """Test validation with collections exceeding max size"""
    # Test with custom small max_size for easier testing
    small_max_size = 5
    
    # Test collection_a too large
    with pytest.raises(CollectionTooLargeException):
        TwoCollectionIntersector([1, 2, 3, 4, 5, 6], [1, 2], max_collection_size=small_max_size)
    
    # Test collection_b too large
    with pytest.raises(CollectionTooLargeException):
        TwoCollectionIntersector([1, 2], [1, 2, 3, 4, 5, 6], max_collection_size=small_max_size)
