from cache.store import LRUStore


def test_lrustore_default_update_hook_moves_to_end() -> None:
    """Test that the default update_hook returns the key and value unchanged and moves the key to the end."""
    store = LRUStore[int](2)
    store["a"] = 1
    store["b"] = 2
    # Call default update_hook
    key, value = store.update_hook("a", 3)
    assert key == "a"
    assert value == 3
    # After update_hook, 'a' should be the most recently used (last key)
    assert list(store.keys())[-1] == "a"


class CustomUpdateHookLRUStore(LRUStore[int]):
    def update_hook(self, key: str, value: int) -> tuple[str, int]:
        # Use super to move to end, then increment value
        super().update_hook(key, value)
        return key, value + 1


def test_lrustore_update_hook_moves_to_end_and_transforms() -> None:
    """Test that a custom update_hook transforms the value and moves the key to the end."""
    store = CustomUpdateHookLRUStore(2)
    store["a"] = 1
    store["b"] = 2
    key, value = store.update_hook("a", 3)
    assert key == "a"
    assert value == 4
    # After update_hook, 'a' should be the most recently used (last key)
    assert list(store.keys())[-1] == "a"
