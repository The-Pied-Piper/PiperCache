from cache.cache import Cache
from cache.tests.fixtures import store_factory, StoreFactoryProtocol
from cache.exceptions import CacheKeyException
import pytest


def test_cache_get_returns_value(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get retrieves the value for an existing key."""
    store = store_factory(2)
    store["a"] = 1
    cache = Cache(store)
    assert cache.get("a") == 1


class CustomGetHookCache(Cache[int]):
    def get_hook(self, key: str, value: int) -> tuple[str, int]:
        return key, value * 2


def test_cache_get_uses_get_hook(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get uses get_hook and its result is returned."""
    store = store_factory(2)
    store["a"] = 2
    cache = CustomGetHookCache(store)
    assert cache.get("a") == 4


def test_cache_get_raises_on_missing(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get raises CacheKeyException if the key is missing."""
    store = store_factory(2)
    cache = Cache(store)
    with pytest.raises(CacheKeyException):
        cache.get("missing")


def test_cache_get_accepts_various_value_types(
    store_factory: StoreFactoryProtocol[object],
) -> None:
    """Test that get works with string keys and values of different types (e.g., int, str, list)."""
    store = store_factory(3)
    store["a"] = 123
    store["b"] = "value"
    store["c"] = [1, 2, 3]
    cache = Cache(store)
    assert cache.get("a") == 123
    assert cache.get("b") == "value"
    assert cache.get("c") == [1, 2, 3]
