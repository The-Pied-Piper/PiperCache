"""Contains tests for the Cache class."""
from uuid import uuid4
from cache.cache import Cache


class TestPut:
    """Test cases for the put function."""

    def test_add_first_data(self):
        """Test adding data when the store is empty."""
        cache = Cache(10)
        key = str(uuid4())
        value = uuid4().hex
        cache.put(key, value)
        assert cache._store[key] == value # pylint: disable=protected-access

    def test_add_data(self):
        """test adding data when the store is not empty."""
        cache = Cache(10)
        cache.put(str(uuid4()), str(uuid4()))
        key = str(uuid4())
        value = uuid4().hex
        cache.put(key, value)
        assert cache._store[key] == value # pylint: disable=protected-access
