from cache.cache import Cache
from cache.tests.fixtures import store_factory, StoreFactoryProtocol


def test_cache_put_hook_default(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that the default put_hook returns key and value unchanged."""
    cache = Cache(store_factory(2))
    assert cache.put_hook("a", 1) == ("a", 1)


class CustomPutHookCache(Cache[int]):
    def put_hook(self, key: str, value: int) -> tuple[str, int]:
        return key.upper(), value + 1


def test_cache_put_hook_custom(store_factory: StoreFactoryProtocol[int]) -> None:
    """Test that a custom put_hook transforms key and value."""
    cache = CustomPutHookCache(store_factory(2))
    assert cache.put_hook("a", 1) == ("A", 2)
