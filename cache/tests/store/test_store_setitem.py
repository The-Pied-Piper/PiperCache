from cache.store import Store
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


def test_setitem_basic(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that __setitem__ adds a new key-value pair to the store."""
    store = store_factory(2)
    store["a"] = 1
    assert store["a"] == 1


def test_setitem_update_existing(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that __setitem__ updates the value for an existing key."""
    store = store_factory(2)
    store["a"] = 1
    store["a"] = 2
    assert store["a"] == 2


def test_setitem_add_new_hook() -> None:
    """Test that __setitem__ uses add_new_hook when adding a new item."""

    class CustomAddNewHookStore(Store[int]):
        def add_new_hook(self, key: str, value: int) -> tuple[str, int]:
            return key + "_new", value + 100

    store = CustomAddNewHookStore(2)
    store["a"] = 1
    assert "a_new" in store
    assert store["a_new"] == 101


def test_setitem_overflow(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that __setitem__ removes the correct item when the store exceeds its size limit."""
    store = store_factory(2)
    store["a"] = 1
    store["b"] = 2
    store["c"] = 3  # should evict 'a'
    assert "a" not in store
    assert "b" in store and "c" in store


def test_setitem_empty_string_key(store_factory: StoreFactoryProtocol[str]) -> None:
    """Test __setitem__ with an empty string as key."""
    store = store_factory(2)
    store[""] = "empty"
    assert store[""] == "empty"


def test_setitem_side_effects() -> None:
    """Test that __setitem__ triggers side effects in custom add_new_hook or update_hook."""

    class SideEffectStore(Store[int]):
        def __init__(self, size: int):
            super().__init__(size)
            self.added = 0
            self.updated = 0

        def add_new_hook(self, key: str, value: int) -> tuple[str, int]:
            self.added += 1
            return key, value

        def update_hook(self, key: str, value: int) -> tuple[str, int]:
            self.updated += 1
            return key, value

    store = SideEffectStore(2)
    store["a"] = 1  # add
    store["a"] = 2  # update
    assert store.added == 1
    assert store.updated == 1


def test_setitem_overridden() -> None:
    """Test that an overridden __setitem__ method is respected."""

    class CustomSetItemStore(Store[int]):
        def __setitem__(self, key: str, value: int) -> None:
            self.custom_called = True

    store = CustomSetItemStore(2)
    store.custom_called = False
    store["a"] = 1
    assert store.custom_called is True
