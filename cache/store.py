"""This module contains the various data store implementations."""

from collections import OrderedDict


from typing import TypeVar, Generic, Tuple, Optional, Iterator


V = TypeVar("V")


class Store(OrderedDict[str, V], Generic[V]):
    """A low level cache implementation."""

    size: int

    def __init__(self, size: int, *args: object, **kwargs: object) -> None:
        self.size = size
        super().__init__(*args, **kwargs)

    def get_overflow(self, _key: str, _value: V) -> str:
        """Get the key of the item to remove if there are too many items."""
        return next(iter(self))

    def add_new_hook(self, key: str, value: V) -> Tuple[str, V]:
        """Run this hook before adding a new item to the store."""
        return key, value

    def update_hook(self, key: str, value: V) -> Tuple[str, V]:
        """Run this hook before updating an existing store item."""
        return key, value

    def get_hook(self, _key: str, value: V) -> V:
        """Run this hook before fetching an item from the store."""
        return value

    def get(self, key: str, default: Optional[V] = None) -> Optional[V]:  # type: ignore[override]
        value = super().get(key, default)
        if value is not None:
            return self.get_hook(key, value)
        return value

    def __getitem__(self, key: str) -> V:
        return self.get_hook(key, super().__getitem__(key))

    def __setitem__(self, key: str, value: V) -> None:
        if key in self:
            key, value = self.update_hook(key, value)
        else:
            if len(self) == self.size:
                del self[self.get_overflow(key, value)]
            key, value = self.add_new_hook(key, value)
        super().__setitem__(key, value)


class LRUStore(Store[V], Generic[V]):
    """A low level LRU cache."""

    def update_hook(self, key: str, value: V) -> Tuple[str, V]:
        """Run this hook before updating an existing store item."""
        self.move_to_end(key)
        return key, value

    def get_hook(self, key: str, value: V) -> V:
        """Run this hook before fetching an item from the store."""
        self.move_to_end(key)
        return value
