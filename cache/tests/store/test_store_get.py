from cache.store import Store
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


def test_get_basic(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get returns the value for an existing key."""
    store = store_factory(2)
    store["a"] = 1
    assert store.get("a") == 1


def test_get_missing_key_returns_none(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get returns None if the key is not present and no default is given."""
    store = store_factory(2)
    assert store.get("missing") is None


def test_get_missing_key_with_default(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that get returns the provided default value if the key is not present."""
    store = store_factory(2)
    assert store.get("missing", 42) == 42


def test_get_empty_string_key(store_factory: StoreFactoryProtocol[str]) -> None:
    """Test get with an empty string as key."""
    store = store_factory(2)
    store[""] = "empty"
    assert store.get("") == "empty"


def test_get_none_default(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test get with None as default value."""
    store = store_factory(2)
    assert store.get("missing", None) is None


def test_get_side_effects() -> None:
    """Test that get triggers side effects in a custom get_hook."""

    class CounterStore(Store[int]):
        def __init__(self, size: int):
            super().__init__(size)
            self.counter = 0

        def get_hook(self, key: str, value: int) -> int:
            self.counter += 1
            return value

    store = CounterStore(2)
    store["a"] = 1
    store.get("a")
    store.get("a")
    assert store.counter == 2


def test_get_overridden() -> None:
    """Test that an overridden get method is respected."""

    class CustomGetStore(Store[int]):
        def get(self, key: str, default: int = 0) -> int:  # type: ignore[override]
            return 12345

    store = CustomGetStore(2)
    store["a"] = 1
    assert store.get("a") == 12345
