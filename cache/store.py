"""This module contains the various data store implementations."""
from collections import OrderedDict


class Store(OrderedDict):
    """A low level cache implementation."""

    def __init__(self, size: int, *args, **kwargs):
        self.size = size
        super().__init__(*args, **kwargs)

    def get_overflow(self):
        """Get the key of the item to remove if there are too many items."""
        return next(iter(self))

    def add_new_hook(self, key, value):
        """Run this hook before adding a new item to the store."""
        return key, value

    def update_hook(self, key, value):
        """Run this hook before updating an existing store item."""
        return key, value

    def get_hook(self, _key, value):
        """Run this hook before fetching an item from the store."""
        return value

    def __getitem__(self, key):
        return self.get_hook(key, super().__getitem__(key))

    def __setitem__(self, key, value) -> None:
        if key in self:
            key, value = self.update_hook(key, value)
        else:
            if len(self) == self.size:
                del self[self.get_overflow()]
            key, value = self.add_new_hook(key, value)
        super().__setitem__(key, value)
