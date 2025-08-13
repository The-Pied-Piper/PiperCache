import pytest
from cache.store import Store
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


def test_getitem_basic(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that __getitem__ returns the value for an existing key."""
    store = store_factory(2)
    store["a"] = 1
    assert store["a"] == 1


def test_getitem_missing_key_raises(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that __getitem__ raises KeyError if the key is not present."""
    store = store_factory(2)
    with pytest.raises(KeyError):
        _ = store["missing"]


def test_getitem_empty_string_key(store_factory: StoreFactoryProtocol[str]) -> None:
    """Test __getitem__ with an empty string as key."""
    store = store_factory(2)
    store[""] = "empty"
    assert store[""] == "empty"


def test_getitem_side_effects() -> None:
    """Test that __getitem__ triggers side effects in a custom get_hook."""

    class CounterStore(Store[int]):
        def __init__(self, size: int):
            super().__init__(size)
            self.counter = 0

        def get_hook(self, key: str, value: int) -> int:
            self.counter += 1
            return value

    store = CounterStore(2)
    store["a"] = 1
    _ = store["a"]
    _ = store["a"]
    assert store.counter == 2


def test_getitem_overridden() -> None:
    """Test that an overridden __getitem__ method is respected."""

    class CustomGetItemStore(Store[int]):
        def __getitem__(self, key: str) -> int:
            return 999

    store = CustomGetItemStore(2)
    store["a"] = 1
    assert store["a"] == 999
