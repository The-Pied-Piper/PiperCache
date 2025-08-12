"""This module contains the various cache implementations."""

from typing import TypeVar, Generic, Tuple
from cache.exceptions import CacheKeyException
from cache.store import Store, LRUStore


V = TypeVar("V")


class Cache(Generic[V]):
    """Base class for caching data."""

    def __init__(self, store: Store[V]):
        self._store: Store[V] = store

    def put_hook(self, key: str, value: V) -> Tuple[str, V]:
        """Overwrite with pre save actions."""
        return key, value

    def get_hook(self, key: str, value: V) -> Tuple[str, V]:
        """Overwrite with pre fetch actions."""
        return key, value

    def put(self, key: str, value: V) -> None:
        """Create or update the value for the given key."""
        key, value = self.put_hook(key, value)
        self._store[key] = value

    def get(self, key: str) -> V:
        """Fetch the value for the given key from the store."""
        try:
            value = self._store[key]
        except KeyError as err:
            raise CacheKeyException("Could not find key in the cache") from err

        _, value = self.get_hook(key, value)
        return value

    def delete(self, key: str) -> None:
        """Delete the data for the given key from the store."""
        self._store.pop(key, None)


class LRUCache(Cache[V], Generic[V]):
    """A simple LRU cache."""

    def __init__(self, size: int) -> None:
        super().__init__(LRUStore(size))
        self._size: int = size

    def reset(self) -> None:
        """Reset the store."""
        self._store = LRUStore(self._size)
