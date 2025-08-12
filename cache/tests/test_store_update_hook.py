import pytest
from cache.store import Store
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


class CustomKeyUpdateStore(Store[str]):
    def update_hook(self, key: str, value: str) -> tuple[str, str]:
        return key.upper(), value


class CustomValueUpdateStore(Store[int]):
    def update_hook(self, key: str, value: int) -> tuple[str, int]:
        return key, value * 2


class CustomBothUpdateStore(Store[int]):
    def update_hook(self, key: str, value: int) -> tuple[str, int]:
        return key + "_updated", value + 100


def test_update_hook_default(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that the default update_hook returns the key and value unchanged."""
    store = store_factory(2)
    store["a"] = 1
    assert store.update_hook("a", 2) == ("a", 2)


def test_update_hook_custom_key() -> None:
    """Test that a custom update_hook can transform the key."""
    store = CustomKeyUpdateStore(2)
    store["foo"] = "bar"
    assert store.update_hook("foo", "baz") == ("FOO", "baz")


def test_update_hook_custom_value() -> None:
    """Test that a custom update_hook can transform the value."""
    store = CustomValueUpdateStore(2)
    store["x"] = 5
    assert store.update_hook("x", 10) == ("x", 20)


def test_update_hook_custom_both() -> None:
    """Test that a custom update_hook can transform both key and value."""
    store = CustomBothUpdateStore(2)
    store["k"] = 1
    assert store.update_hook("k", 1) == ("k_updated", 101)


def test_update_hook_integration() -> None:
    """Test that update_hook is used when updating an existing item in the store."""
    store = CustomBothUpdateStore(2)
    store["a"] = 1
    store["a"] = 2  # triggers update_hook
    assert "a_updated" in store
    assert store["a_updated"] == 102


def test_update_hook_edge_cases(store_factory: StoreFactoryProtocol[str]) -> None:
    """Test update_hook with empty string key and value."""
    store = store_factory(2)
    store[""] = ""
    assert store.update_hook("", "") == ("", "")
