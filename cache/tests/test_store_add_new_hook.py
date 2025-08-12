import pytest
from cache.store import Store
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


class CustomKeyStore(Store[str]):
    def add_new_hook(self, key: str, value: str) -> tuple[str, str]:
        return key.upper(), value


class CustomValueStore(Store[int]):
    def add_new_hook(self, key: str, value: int) -> tuple[str, int]:
        return key, value * 2


class CustomBothStore(Store[int]):
    def add_new_hook(self, key: str, value: int) -> tuple[str, int]:
        return key + "_new", value + 100


def test_add_new_hook_default(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that the default add_new_hook returns the key and value unchanged."""
    store = store_factory(2)
    assert store.add_new_hook("a", 1) == ("a", 1)


def test_add_new_hook_custom_key() -> None:
    """Test that a custom add_new_hook can transform the key."""
    store = CustomKeyStore(2)
    assert store.add_new_hook("foo", "bar") == ("FOO", "bar")


def test_add_new_hook_custom_value() -> None:
    """Test that a custom add_new_hook can transform the value."""
    store = CustomValueStore(2)
    assert store.add_new_hook("x", 5) == ("x", 10)


def test_add_new_hook_custom_both() -> None:
    """Test that a custom add_new_hook can transform both key and value."""
    store = CustomBothStore(2)
    assert store.add_new_hook("k", 1) == ("k_new", 101)


def test_add_new_hook_integration() -> None:
    """Test that add_new_hook is used when adding a new item to the store."""
    store = CustomBothStore(2)
    store["a"] = 1
    assert "a_new" in store
    assert store["a_new"] == 101


def test_add_new_hook_edge_cases(store_factory: StoreFactoryProtocol[str]) -> None:
    """Test add_new_hook with empty string key and value."""
    store = store_factory(2)
    assert store.add_new_hook("", "") == ("", "")
