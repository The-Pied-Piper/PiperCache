from cache.cache import Cache
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


class CustomGetHookCache(Cache[int]):
    def get_hook(self, key: str, value: int) -> tuple[str, int]:
        return key, value * 2


def test_cache_get_hook_default(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that the default get_hook returns key and value unchanged."""
    cache = Cache(store_factory(2))
    assert cache.get_hook("a", 1) == ("a", 1)


def test_cache_get_hook_custom(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that a custom get_hook transforms key and value."""
    cache = CustomGetHookCache(store_factory(2))
    assert cache.get_hook("a", 2) == ("a", 4)
