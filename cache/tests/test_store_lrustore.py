"""Contains tests for the LRUStore class."""
from cache.store import LRUStore


class TestUpdateHook:
    """Tests  for the `update_hook` function."""

    def test_element_moved_to_end(self):
        """test that the update_hook moves an element moves it to the end."""
        store = LRUStore(10)
        key1 = "key1"
        key2 = "key2"
        key3 = "key3"
        value1 = "value1"
        value2 = "value2"
        value3 = "value3"
        value4 = "value4"
        store[key1] = value1
        store[key2] = value2
        store[key3] = value3
        store.update_hook(key1, value4)
        assert list(store.keys())[-1] == key1
        assert list(store.keys())[0] == key2

    def test_return(self):
        """test that the update_hook returns (key, value)."""
        store = LRUStore(10)
        key1 = "key1"
        value1 = "value1"
        value2 = "value2"
        store[key1] = value1
        test_key, test_value = store.update_hook(key1, value2)
        assert test_key == key1 and test_value == value2


class TestGetHook:
    """Tests  for the `get_hook` function."""

    def test_element_moved_to_end(self):
        """test that the get_hook moves an element moves it to the end."""
        store = LRUStore(10)
        key1 = "key1"
        key2 = "key2"
        key3 = "key3"
        value1 = "value1"
        value2 = "value2"
        value3 = "value3"
        store[key1] = value1
        store[key2] = value2
        store[key3] = value3
        store.get_hook(key1, value1)
        assert list(store.keys())[-1] == key1
        assert list(store.keys())[0] == key2

    def test_return(self):
        """test that the get_hook returns the value argument."""
        store = LRUStore(10)
        key1 = "key1"
        value1 = "value1"
        value2 = "value2"
        store[key1] = value1
        assert store.get_hook(key1, value2) == value2
