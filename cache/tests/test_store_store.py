"""Containts tests for the Store class."""
from unittest.mock import MagicMock

from cache.store import Store

class TestGetItem:
    """Tests for the `__getitem__` function."""

    def test_get(self):
        """Test getting the value for a key."""
        store = Store(10)
        key = "key1"
        value = "value1"
        store[key] = value
        store.get_hook = MagicMock(return_value = value)
        assert store[key] == value
        store.get_hook.assert_called_once_with(key, value)


class TestGet:
    """Tests for the `get` function."""

    def test_get(self):
        """Test getting the value for a key."""
        store = Store(10)
        key = "key1"
        value = "value1"
        store[key] = value
        store.get_hook = MagicMock(return_value = value)
        assert store.get(key) == value
        store.get_hook.assert_called_once_with(key, value)


class TestSetItem:
    """Tests for the `__setitem__` function."""

    def test_item_is_set(self):
        """Test that the value is set properly."""
        store = Store(10)
        key = "key1"
        value = "value1"
        store[key] = value
        assert store[key] == value

    def test_add_new_item(self):
        """test adding a new item."""
        store = Store(10)
        key = "key1"
        value = "value1"
        store.add_new_hook = MagicMock(return_value = (key, value))
        store.update_hook = MagicMock(return_value = (key, value))
        store[key] = value
        store.add_new_hook.assert_called_once_with(key, value)
        store.update_hook.assert_not_called()

    def test_update(self):
        """test updating an existing key."""
        store = Store(10)
        key = "key1"
        value1 = "value1"
        value2 = "value2"
        store.update_hook = MagicMock(return_value = (key, value1))
        store[key] = value1
        store.add_new_hook = MagicMock(return_value = (key, value1))
        store[key] = value2
        store.update_hook.assert_called_once_with(key, value2)
        store.add_new_hook.assert_not_called()

    def test_overflow(self):
        """test setting an item when store is full."""
        store = Store(1)
        key1 = "key1"
        key2 = "key2"
        value1 = "value1"
        value2 = "value2"
        store[key1] = value1
        store.get_overflow = MagicMock(return_value = key1)
        store.add_new_hook = MagicMock(return_value = (key2, value2))
        store[key2] = value2
        store.get_overflow.assert_called_once_with(key2, value2)
        store.add_new_hook.assert_called_once_with(key2, value2)

    def test_get_overflow_not_called(self):
        """Test that get_overflow function is not called if store has room."""
        store = Store(10)
        key1 = "key1"
        value1 = "value1"
        key2 = "key2"
        value2 = "value2"
        store[key1] = value1
        store.get_overflow = MagicMock(return_value = key1)
        store[key2] = value2
        store.get_overflow.assert_not_called()

    def test_full_update(self):
        """Test updating the store when it is full."""
        store = Store(1)
        key = "key1"
        value1 = "value1"
        value2 = "value2"
        store[key] = value1
        store.get_overflow = MagicMock(return_value = key)
        store.update_hook = MagicMock(return_value = (key, value2))
        store[key] = value2
        store.get_overflow.assert_not_called()
        store.update_hook.assert_called_once_with(key, value2)

    def test_del(self):
        """Test that the store deletes the overflow item."""
        store = Store(1)
        key1 = "key1"
        key2 = "key2"
        value1 = "value1"
        value2 = "value2"
        store[key1] = value1
        store.get_overflow = MagicMock(return_value = key1)
        store[key2] = value2
        assert key1 not in store

class TestGetOverflow():
    """tests for the `get_over_flow` function."""

    def test_get_first_item(self):
        """test that get_overflow returns the first added key."""
        store = Store(10)
        key1 = "key1"
        key2 = "key2"
        key3 = "key3"
        value1 = "value1"
        value2 = "value2"
        value3 = "value3"
        store[key1] = value1
        store[key2] = value2
        store[key3] = value3
        assert store.get_overflow("key4", "value4") == key1
