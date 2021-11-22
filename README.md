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