import pytest

from tasks_executor import batched


def test_normal_case():
    iterable = 'ABCDEFG'
    batch_size = 3
    result = list(batched(iterable, batch_size))
    expected = [('A', 'B', 'C'), ('D', 'E', 'F'), ('G',)]
    assert result == expected


def test_empty_iterable():
    iterable = ''
    batch_size = 3
    result = list(batched(iterable, batch_size))
    expected = []
    assert result == expected


def test_batch_size_greater_than_iterable_length():
    iterable = 'ABC'
    batch_size = 5
    result = list(batched(iterable, batch_size))
    expected = [('A', 'B', 'C')]
    assert result == expected


def test_invalid_batch_size():
    iterable = 'ABCDEFG'
    batch_size = 0
    with pytest.raises(ValueError):
        list(batched(iterable, batch_size))


def test_single_element_batching():
    iterable = 'ABCDEFG'
    batch_size = 1
    result = list(batched(iterable, batch_size))
    expected = [('A',), ('B',), ('C',), ('D',), ('E',), ('F',), ('G',)]
    assert result == expected


def test_batch_size_equal_iterable_length():
    iterable = 'ABCDE'
    batch_size = 5
    result = list(batched(iterable, batch_size))
    expected = [('A', 'B', 'C', 'D', 'E')]
    assert result == expected


def test_batch_size_one():
    iterable = 'ABCDEFG'
    batch_size = 1
    result = list(batched(iterable, batch_size))
    expected = [('A',), ('B',), ('C',), ('D',), ('E',), ('F',), ('G',)]
    assert result == expected


if __name__ == "__main__":
    pytest.main()
