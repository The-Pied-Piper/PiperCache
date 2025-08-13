from cache.store import LRUStore
import pytest


def test_lrustore_getitem_missing_key_raises() -> None:
    """Test that __getitem__ raises KeyError if the key is not present."""
    store = LRUStore[int](2)
    with pytest.raises(KeyError):
        _ = store["missing"]
