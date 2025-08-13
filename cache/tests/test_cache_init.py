from cache.cache import Cache
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


def test_cache_init_sets_store(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that Cache initializes with the given Store instance."""
    store = store_factory(2)
    cache = Cache(store)
    assert cache._store is store
