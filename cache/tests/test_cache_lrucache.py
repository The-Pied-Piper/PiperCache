"""Contains tests for the LRUCache class."""
from cache.cache import LRUCache

class TestReset:
    """Tests for the `reset` function."""

    def test_empty_store(self):
        """tests that the reset function empties the store."""
        cache = LRUCache(2)
        key1 = "key1"
        key2 = "key2"
        value1 = "value1"
        value2 = "value2"
        cache.put(key1, value1)
        cache.put(key2, value2)
        assert len(cache._store) == 2 # pylint: disable=protected-access
        cache.reset()
        assert len(cache._store) == 0 # pylint: disable=protected-access

    def test_add_after_reset(self):
        """tests adding data after reset."""
        cache = LRUCache(2)
        key1 = "key1"
        key2 = "key2"
        value1 = "value1"
        value2 = "value2"
        cache.put(key1, value1)
        cache.put(key2, value2)
        assert len(cache._store) == 2 # pylint: disable=protected-access
        cache.reset()
        assert len(cache._store) == 0 # pylint: disable=protected-access
        cache.put(key1, value1)
        cache.put(key2, value2)
        assert len(cache._store) == 2 # pylint: disable=protected-access
