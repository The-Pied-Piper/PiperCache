from cache.cache import LRUCache
from cache.exceptions import CacheKeyException
import pytest


def test_lrucache_basic_put_get() -> None:
    """Test basic put and get operations."""
    cache = LRUCache[int](2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    assert cache.get("b") == 2


def test_lrucache_lru_eviction() -> None:
    """Test that least recently used item is evicted."""
    cache = LRUCache[int](2)
    cache.put("x", 10)
    cache.put("y", 20)
    cache.get("x")  # access 'x', now 'y' is LRU
    cache.put("z", 30)  # should evict 'y'
    with pytest.raises(CacheKeyException):
        cache.get("y")
    assert cache.get("x") == 10
    assert cache.get("z") == 30


def test_lrucache_delete() -> None:
    """Test delete functionality."""
    cache = LRUCache[int](2)
    cache.put("a", 1)
    cache.delete("a")
    # Explicitly check that 'a' is not in the store
    assert "a" not in cache._store
    with pytest.raises(CacheKeyException):
        cache.get("a")


def test_lrucache_get_raises_on_missing() -> None:
    """Test that get raises CacheKeyException for missing key."""
    cache = LRUCache[int](2)
    with pytest.raises(CacheKeyException):
        cache.get("missing")


def test_lrucache_hooks() -> None:
    """Test put_hook and get_hook functionality."""

    class CustomLRUCache(LRUCache[int]):
        def put_hook(self, key: str, value: int) -> tuple[str, int]:
            return key.upper(), value + 1

        def get_hook(self, key: str, value: int) -> tuple[str, int]:
            return key, value * 2

    cache = CustomLRUCache(2)
    cache.put("a", 1)
    assert cache.get("A") == 4


def test_lrucache_different_value_types() -> None:
    """Test that LRUCache works with different value types."""
    cache = LRUCache[object](2)
    cache.put("a", 123)
    cache.put("b", [1, 2, 3])
    assert cache.get("a") == 123
    assert cache.get("b") == [1, 2, 3]


def test_lrucache_order_after_multiple_operations() -> None:
    """Test LRU order after multiple operations."""
    cache = LRUCache[int](3)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.put("c", 3)
    cache.get("a")  # access 'a', now order: b, c, a
    cache.put("b", 20)  # update 'b', now order: c, a, b
    cache.get("c")  # access 'c', now order: a, b, c
    cache.put("d", 4)  # should evict 'a', order: b, c, d
    with pytest.raises(CacheKeyException):
        cache.get("a")
    assert cache.get("b") == 20
    assert cache.get("c") == 3
    assert cache.get("d") == 4
