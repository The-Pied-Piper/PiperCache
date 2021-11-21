"""This module contains the various cache implementations."""
from typing import Optional
from cache.store import Store


class Cache:
    """Base class for caching data."""

    def __init__(self, size, store: Optional[Store] = None):
        self._store = store or Store()
        self._size = size

    def pre_put_hook(self, key, value):
        """Overwrite with any pre save actions."""
        return key, value

    def post_put_hook(self, key, value):
        """"Overwrite with any post save actions."""

    def put(self, key, value):
        """Create or update the value for the given key."""
        key, value = self.pre_put_hook(key, value)
        self._store[key] = value
        self.post_put_hook(key, value)

    def get(self, key):
        """Fetch the value for the given key from the store."""
        return self._store.get(key)

    def delete(self, key):
        """Delete the data for the given key from the store."""
        self._store.pop(key)

# TODO
#     - handle error if key is not found in get method.
#     - handle error if key is not fount in del method.
