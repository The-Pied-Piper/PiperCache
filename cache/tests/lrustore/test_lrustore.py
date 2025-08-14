from cache.store import LRUStore


def test_lrustore_basic_operations() -> None:
    """Test basic put/get operations and LRU behavior."""
    store = LRUStore[int](2)
    store["a"] = 1
    store["b"] = 2
    assert store["a"] == 1
    assert store["b"] == 2
    store["c"] = 3  # should evict 'a'
    assert "a" not in store
    assert "b" in store and "c" in store


def test_lrustore_update_moves_to_end() -> None:
    """Test that updating an item moves it to the end (most recently used)."""
    store = LRUStore[int](2)
    store["a"] = 1
    store["b"] = 2
    store["a"] = 3  # update 'a', now 'b' is LRU
    store["c"] = 4  # should evict 'b'
    assert "b" not in store
    assert "a" in store and store["a"] == 3
    assert "c" in store


def test_lrustore_access_moves_to_end() -> None:
    """Test that accessing an item moves it to the end (most recently used)."""
    store = LRUStore[int](2)
    store["a"] = 1
    store["b"] = 2
    _ = store["a"]  # access 'a', now 'b' is LRU
    store["c"] = 3  # should evict 'b'
    assert "b" not in store
    assert "a" in store and "c" in store


def test_lrustore_different_value_types() -> None:
    """Test that LRUStore works with different value types."""
    store = LRUStore[object](2)
    store["a"] = 123
    store["b"] = "value"
    assert store["a"] == 123
    assert store["b"] == "value"
    store["c"] = [1, 2, 3]
    assert "a" not in store
    assert store["c"] == [1, 2, 3]


def test_lrustore_order_after_multiple_operations() -> None:
    """Test that LRUStore maintains correct order after multiple operations."""
    store = LRUStore[int](3)
    store["a"] = 1
    store["b"] = 2
    store["c"] = 3
    _ = store["a"]  # access 'a', now order: b, c, a
    store["b"] = 20  # update 'b', now order: c, a, b
    _ = store["c"]  # access 'c', now order: a, b, c
    store["d"] = 4  # should evict 'a', order: b, c, d
    assert list(store.keys()) == ["b", "c", "d"]
