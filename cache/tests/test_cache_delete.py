from cache.cache import Cache
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


def test_cache_delete_removes_key(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that delete removes an existing key from the store."""
    store = store_factory(2)
    store["a"] = 1
    cache = Cache(store)
    cache.delete("a")
    assert "a" not in store


def test_cache_delete_no_error_on_missing(
    store_factory: StoreFactoryProtocol[int],
) -> None:
    """Test that delete does nothing if the key does not exist."""
    store = store_factory(2)
    cache = Cache(store)
    # Should not raise
    cache.delete("missing")


def test_cache_delete_then_get_raises(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that after deletion, get raises CacheKeyException for that key."""
    from cache.exceptions import CacheKeyException

    store = store_factory(2)
    store["a"] = 1
    cache = Cache(store)
    cache.delete("a")
    import pytest

    with pytest.raises(CacheKeyException):
        cache.get("a")
