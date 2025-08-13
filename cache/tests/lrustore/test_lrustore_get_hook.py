from cache.store import LRUStore


def test_lrustore_default_get_hook_moves_to_end() -> None:
    """Test that the default get_hook returns the value unchanged and moves the key to the end."""
    store = LRUStore[int](2)
    store["a"] = 1
    store["b"] = 2
    # Call default get_hook
    result = store.get_hook("a", 1)
    assert result == 1
    # After get_hook, 'a' should be the most recently used (last key)
    assert list(store.keys())[-1] == "a"


class CustomGetHookLRUStore(LRUStore[int]):
    def get_hook(self, key: str, value: int) -> int:
        # Use super to move to end, then double value
        super().get_hook(key, value)
        return value * 2


def test_lrustore_get_hook_moves_to_end_and_transforms() -> None:
    """Test that a custom get_hook transforms the value and moves the key to the end."""
    store = CustomGetHookLRUStore(2)
    store["a"] = 1
    store["b"] = 2
    result = store.get_hook("a", 1)
    assert result == 2
    # After get_hook, 'a' should be the most recently used (last key)
    assert list(store.keys())[-1] == "a"
