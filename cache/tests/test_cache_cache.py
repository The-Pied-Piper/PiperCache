"""Contains tests for the Cache class."""
from unittest.mock import MagicMock

from cache.cache import Cache
from cache.store import Store


class TestPut:
    """Test cases for the `put` function."""

    def test_add_first_data(self):
        """Test adding data when the store is empty."""
        store = Store(10)
        cache = Cache(store)
        key = "key1"
        value = "value1"
        cache.put(key, value)
        assert store[key] == value

    def test_add_data(self):
        """Test adding data when the store is not empty."""
        store = Store(10)
        store["key1"] = "value1"
        cache = Cache(store)
        key = "key2"
        value = "value2"
        cache.put(key, value)
        assert store[key] == value

    def test_update_data(self):
        """Test updating a value for an existing key."""
        store = Store(10)
        key = "key1"
        store[key] = "value1"
        cache = Cache(store)
        value = "value2"
        cache.put(key, value)
        assert store[key] == value

    def test_put_hook_called(self):
        """Test that the put hook is called correctly."""
        store = Store(10)
        key = "key1"
        value = "value1"
        cache = Cache(store)
        cache.put_hook = MagicMock(return_value = (key, value))
        cache.put(key, value)
        cache.put_hook.assert_called_once_with(key, value)


class TestGet:
    """Test the `get` function."""

    def test_get(self):
        """Test getting cached data."""
        store = Store(10)
        key = "key1"
        value = "value1"
        store[key] = value
        cache = Cache(store)
        assert cache.get(key) == value

    def test_get_hook_called(self):
        """Test getting cached data."""
        store = Store(10)
        key = "key1"
        value = "value1"
        store[key] = value
        cache = Cache(store)
        cache.get_hook = MagicMock(return_value = (key, value))
        cache.get(key)
        cache.get_hook.assert_called_once_with(key, value)

class TestDelete:
    """Tests for the delete function."""

    def test_removes_item(self):
        """test that the item is removed."""
        store = Store(10)
        key1 = "key1"
        key2 = "key2"
        value1 = "value1"
        value2 = "value2"
        store[key1] = value1
        store[key2] = value2
        cache = Cache(store)
        cache.delete(key1)
        assert key1 not in store

    def test_remove_last_item(self):
        """test removing the last item."""
        store = Store(10)
        key1 = "key1"
        value1 = "value1"
        store[key1] = value1
        cache = Cache(store)
        cache.delete(key1)
        assert key1 not in store

    def test_remove_not_in_store(self):
        """test removing the last item."""
        store = Store(10)
        key1 = "key1"
        key2 = "key2"
        key3 = "key3"
        value1 = "value1"
        value2 = "value2"
        store[key1] = value1
        store[key2] = value2
        cache = Cache(store)
        cache.delete(key3)
        assert key1 in store
        assert key2 in store
        assert key3 not in store
