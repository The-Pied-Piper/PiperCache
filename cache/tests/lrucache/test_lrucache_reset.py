from cache.cache import LRUCache


def test_lrucache_reset() -> None:
    """Test that reset clears the cache and restores the size."""
    cache: LRUCache[int] = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    cache.reset()
    # After reset, cache should be empty
    with_cache_key_exception = False
    try:
        cache.get("a")
    except Exception:
        with_cache_key_exception = True
    assert with_cache_key_exception
    cache.put("c", 3)
    cache.put("d", 4)
    assert cache.get("c") == 3
    assert cache.get("d") == 4
