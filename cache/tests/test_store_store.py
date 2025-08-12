"""Containts tests for the Store class."""

from unittest.mock import MagicMock, patch

from cache.store import Store


class TestGetItem:
    """Tests for the `__getitem__` function."""

    def test_get(self) -> None:
        """Test getting the value for a key."""
        store = Store[str](10)
        key = "key1"
        value = "value1"
        store[key] = value
        with patch.object(store, "get_hook", return_value=value) as mock_get_hook:
            assert store[key] == value
            mock_get_hook.assert_called_once_with(key, value)


class TestGet:
    """Tests for the `get` function."""

    def test_get(self) -> None:
        """Test getting the value for a key."""
        store = Store[str](10)
        key = "key1"
        value = "value1"
        store[key] = value
        with patch.object(store, "get_hook", return_value=value) as mock_get_hook:
            assert store.get(key) == value
            mock_get_hook.assert_called_once_with(key, value)


class TestSetItem:
    """Tests for the `__setitem__` function."""

    def test_item_is_set(self) -> None:
        """Test that the value is set properly."""
        store = Store[str](10)
        key = "key1"
        value = "value1"
        store[key] = value
        assert store[key] == value

    def test_add_new_item(self) -> None:
        """test adding a new item."""
        store = Store[str](10)
        key = "key1"
        value = "value1"
        with patch.object(
            store, "add_new_hook", return_value=(key, value)
        ) as mock_add_new_hook, patch.object(
            store, "update_hook", return_value=(key, value)
        ) as mock_update_hook:
            store[key] = value
            mock_add_new_hook.assert_called_once_with(key, value)
            mock_update_hook.assert_not_called()

    def test_update(self) -> None:
        """test updating an existing key."""
        store = Store[str](10)
        key = "key1"
        value1 = "value1"
        value2 = "value2"
        with patch.object(
            store, "update_hook", return_value=(key, value1)
        ) as mock_update_hook:
            store[key] = value1
            with patch.object(
                store, "add_new_hook", return_value=(key, value1)
            ) as mock_add_new_hook:
                store[key] = value2
                mock_update_hook.assert_called_once_with(key, value2)
                mock_add_new_hook.assert_not_called()

    def test_overflow(self) -> None:
        """test setting an item when store is full."""
        store = Store[str](1)
        key1 = "key1"
        key2 = "key2"
        value1 = "value1"
        value2 = "value2"
        store[key1] = value1
        with patch.object(
            store, "get_overflow", return_value=key1
        ) as mock_get_overflow, patch.object(
            store, "add_new_hook", return_value=(key2, value2)
        ) as mock_add_new_hook:
            store[key2] = value2
            mock_get_overflow.assert_called_once_with(key2, value2)
            mock_add_new_hook.assert_called_once_with(key2, value2)

    def test_get_overflow_not_called(self) -> None:
        """Test that get_overflow function is not called if store has room."""
        store = Store[str](10)
        key1 = "key1"
        value1 = "value1"
        key2 = "key2"
        value2 = "value2"
        store[key1] = value1
        with patch.object(
            store, "get_overflow", return_value=key1
        ) as mock_get_overflow:
            store[key2] = value2
            mock_get_overflow.assert_not_called()

    def test_full_update(self) -> None:
        """Test updating the store when it is full."""
        store = Store[str](1)
        key = "key1"
        value1 = "value1"
        value2 = "value2"
        store[key] = value1
        with patch.object(
            store, "get_overflow", return_value=key
        ) as mock_get_overflow, patch.object(
            store, "update_hook", return_value=(key, value2)
        ) as mock_update_hook:
            store[key] = value2
            mock_get_overflow.assert_not_called()
            mock_update_hook.assert_called_once_with(key, value2)

    def test_del(self) -> None:
        """Test that the store deletes the overflow item."""
        store = Store[str](1)
        key1 = "key1"
        key2 = "key2"
        value1 = "value1"
        value2 = "value2"
        store[key1] = value1
        with patch.object(store, "get_overflow", return_value=key1):
            store[key2] = value2
            assert key1 not in store


class TestGetOverflow:
    """tests for the `get_over_flow` function."""

    def test_get_first_item(self) -> None:
        """test that get_overflow returns the first added key."""
        store = Store[str](10)
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
