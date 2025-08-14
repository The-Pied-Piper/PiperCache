import pytest
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


def test_get_overflow_basic(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get_overflow returns the first inserted key when the store is full."""
    store = store_factory(2)
    store["a"] = 1
    store["b"] = 2
    assert store.get_overflow("c", 3) == "a"


def test_get_overflow_single_item(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get_overflow returns the only key when the store has one item."""
    store = store_factory(1)
    store["x"] = 42
    assert store.get_overflow("y", 99) == "x"


def test_get_overflow_empty(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get_overflow raises StopIteration when the store is empty."""
    store = store_factory(1)
    with pytest.raises(StopIteration):
        store.get_overflow("any", 0)


def test_get_overflow_multiple_items(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get_overflow returns the oldest key when multiple items are present."""
    store = store_factory(3)
    store["first"] = 1
    store["second"] = 2
    store["third"] = 3
    assert store.get_overflow("fourth", 4) == "first"


def test_get_overflow_ignores_args(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get_overflow ignores its arguments and always returns the first key."""
    store = store_factory(2)
    store["foo"] = 10
    store["bar"] = 20
    # Should always return the first key, regardless of _key/_value
    assert store.get_overflow("baz", 999) == "foo"
