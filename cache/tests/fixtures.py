import pytest
from typing import TypeVar, Protocol, Any, Type
from cache.store import Store


T = TypeVar("T")


class StoreFactoryProtocol(Protocol[T]):
    def __call__(self, size: int, *args: Any, **kwargs: Any) -> Store[T]: ...


@pytest.fixture
def store_factory() -> StoreFactoryProtocol[T]:
    def _factory(size: int) -> Store[T]:

        class _Store(Store[T]):
            pass

        return _Store(size)

    return _factory
