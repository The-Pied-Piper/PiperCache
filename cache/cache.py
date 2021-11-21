"""This module contains the various cache implementations."""
from cache.store import Store, LRUStore


class Cache:
    """Base class for caching data."""

    def __init__(self, store: Store):
        self._store = store

    def put_hook(self, key, value):
        """Overwrite with pre save actions."""
        return key, value

    def get_hook(self, key, value):
        """Overwrite with pre fetch actions."""
        return key, value

    def put(self, key, value):
        """Create or update the value for the given key."""
        key, value = self.put_hook(key, value)
        self._store[key] = value

    def get(self, key):
        """Fetch the value for the given key from the store."""
        _, value = self.get_hook(key, self._store[key])
        return value

    def delete(self, key):
        """Delete the data for the given key from the store."""
        self._store.pop(key, None)

class LRUCache(Cache):
    """A simple LRU cache."""

    def __init__(self, size):
        super().__init__(LRUStore(size))
        self._size = size

    def reset(self):
        """Reset the store."""
        self.__init__(LRUStore(self._size))

# TODO
#     - handle error if key is not found in get method.
