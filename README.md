# Piper Cache

This library provides an easy and extendable way to create a cache in python.

## Getting Started

To install the package for use in your code you can use pip
```
pip install git+ssh://git@github.com:The-Pied-Piper/PiperCache.git#egg=cache
```

For local development you can use `pipenv` (see pipenv documentation for how to install pipenv):
```
pipenv install --dev
```

## Usage
To use the build in caches:
```python3
from cache.cache import LRUCache

lru_cache = LRUCache(10)
lru_cache.put("key1", "value1")
lru_cache.put("key2", "value2")
lru_cache.get("key1")  # "value1"

lru_cache.delete("key2)
lry_cache.get("key2")  # Exception

lru_cache.reset()
lru_cache.get("key1")  # Exception
```

**Or** construct your own:
```python3
from cache.store import Store
from cache.cache import Cache

class MyStore(Store):
    """My class to extend store logic."""
    # ...

class MyCache(Cache)
    """My class to extend the Cache API."""

    def __init__(self):
        store = MyStore()
        super().__init__(store)

    # ...
```

**Or** mix and match build in stores and caches.