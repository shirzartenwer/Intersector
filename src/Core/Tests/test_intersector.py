from Core.two_collection_intersector import TwoCollectionIntersector
import pytest


@pytest.mark.parametrize("size_a, size_b", [(100, 200), (0, 0), (1, 1), (50, 50)])
def test_initialization(size_a, size_b):
    intersector = TwoCollectionIntersector.from_sizes(size_a, size_b)
    assert len(intersector.collection_a) == size_a
    assert len(intersector.collection_b) == size_b


def test_output_number_type(size_a=100, size_b=200):
    intersector = TwoCollectionIntersector.from_sizes(size_a, size_b)
    result, run_time = intersector.intersect("Collection A")
    assert isinstance(result, list)
    assert all(isinstance(x, float) for x in result)
    assert isinstance(run_time, float)

    
@pytest.mark.parametrize("size_a, size_b, collection, expected_length", 
                          [(0, 100, "Collection A", 0), 
                           (100, 0, "Collection B", 0), 
                           (0, 0, "Collection A", 0),
                           (0, 0, "Collection B", 0)])
def test_intersect_empty_collections(size_a, size_b, expected_length, collection):
    intersector = TwoCollectionIntersector.from_sizes(size_a, size_b)
    result, run_time = intersector.intersect(collection)
    assert len(result) == expected_length
    assert run_time >= 0.0



@pytest.mark.parametrize("collection_a, collection_b, choice, expected_length", 
                          [([1.0, 2.0, 3.0], [4.0, 5.0, 6.0], "Collection A", 0),
                           ([1.0, 2.0, 3.0], [4.0, 5.0, 6.0], "Collection B", 0)])
        
def test_intersect_no_common_elements(collection_a, collection_b, choice, expected_length):
    intersector = TwoCollectionIntersector(collection_a, collection_b)
    result, run_time = intersector.intersect(choice)
    assert len(result) == expected_length
    assert run_time >= 0.0



@pytest.mark.parametrize("collection_a, collection_b, choice, expected_length", 
                          [([1.0, 2.0, 3.0], [3.0, 5.0, 6.0], "Collection A", 1),
                           ([1.0, 2.0, 3.0], [3.0, 5.0, 6.0], "Collection B", 1),
                           ([1.0, 2.0, 4.0], [1.0, 2.0, 3.0], "Collection A", 2),
                           ([1.0, 2.0, 4.0], [1.0, 2.0, 3.0], "Collection B", 2)])
        
def test_intersect_some_common_elements(collection_a, collection_b, choice, expected_length):
    intersector = TwoCollectionIntersector(collection_a, collection_b)
    result, run_time = intersector.intersect(choice)
    assert len(result) == expected_length
    assert run_time >= 0.0
