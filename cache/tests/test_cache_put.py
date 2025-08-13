from cache.cache import Cache
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


def test_cache_put_adds_new(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that put adds a new key-value pair to the store."""
    store = store_factory(2)
    cache = Cache(store)
    cache.put("a", 1)
    assert store["a"] == 1


def test_cache_put_updates_existing(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that put updates the value for an existing key."""
    store = store_factory(2)
    cache = Cache(store)
    cache.put("a", 1)
    cache.put("a", 2)
    assert store["a"] == 2


class CustomPutHookCache(Cache[int]):
    def put_hook(self, key: str, value: int) -> tuple[str, int]:
        return key.upper(), value + 1


def test_cache_put_uses_put_hook(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that put uses put_hook and its result is used for storage."""
    store = store_factory(2)
    cache = CustomPutHookCache(store)
    cache.put("a", 1)
    assert "A" in store and store["A"] == 2


def test_cache_put_accepts_various_value_types(
    store_factory: StoreFactoryProtocol[object],
) -> None:
    """Test that put works with string keys and values of different types (e.g., int, str, list)."""
    store = store_factory(3)
    cache = Cache(store)
    cache.put("a", 123)
    cache.put("b", "value")
    cache.put("c", [1, 2, 3])
    assert store["a"] == 123
    assert store["b"] == "value"
    assert store["c"] == [1, 2, 3]
