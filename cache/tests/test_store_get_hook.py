import pytest
from cache.store import Store
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


class CustomGetHookStore(Store[str]):
    def get_hook(self, key: str, value: str) -> str:
        return value.upper()


class KeyConcatGetHookStore(Store[str]):
    def get_hook(self, key: str, value: str) -> str:
        return f"{value}-{key}"


class SideEffectGetHookStore(Store[int]):
    def __init__(self, size: int):
        super().__init__(size)
        self.access_count = 0

    def get_hook(self, key: str, value: int) -> int:
        self.access_count += 1
        return value


def test_get_hook_default(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that the default get_hook returns the value unchanged."""
    store = store_factory(2)
    store["a"] = 1
    assert store.get_hook("a", 1) == 1


def test_get_hook_custom_value() -> None:
    """Test that a custom get_hook can transform the value."""
    store = CustomGetHookStore(2)
    store["foo"] = "bar"
    assert store.get_hook("foo", "bar") == "BAR"


def test_get_hook_key_concat() -> None:
    """Test that get_hook can use the key to transform the value."""
    store = KeyConcatGetHookStore(2)
    store["x"] = "y"
    assert store.get_hook("x", "y") == "y-x"


def test_get_hook_integration_get() -> None:
    """Test that get_hook is used when retrieving an item with get()."""

    class UpperGetHookStore(Store[str]):
        def get_hook(self, key: str, value: str) -> str:
            return value.upper()

    store = UpperGetHookStore(2)
    store["a"] = "b"
    assert store.get("a") == "B"


def test_get_hook_integration_getitem() -> None:
    """Test that get_hook is used when retrieving an item with __getitem__."""

    class UpperGetHookStore(Store[str]):
        def get_hook(self, key: str, value: str) -> str:
            return value.upper()

    store = UpperGetHookStore(2)
    store["a"] = "b"
    assert store["a"] == "B"


def test_get_hook_edge_cases(store_factory: StoreFactoryProtocol[str]) -> None:
    """Test get_hook with empty string key and value."""
    store = store_factory(2)
    assert store.get_hook("", "") == ""


def test_get_hook_multiple_accesses() -> None:
    """Test that get_hook is called every time an item is accessed."""
    store = SideEffectGetHookStore(2)
    store["a"] = 1
    _ = store["a"]
    _ = store["a"]
    assert store.access_count == 2
