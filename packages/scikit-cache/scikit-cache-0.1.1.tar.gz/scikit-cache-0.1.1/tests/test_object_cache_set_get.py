import pytest
from pydantic import BaseModel

from scikit_cache.resources import CacheKey


class User(BaseModel):
    name: str
    age: int

# `get`, `set`, `delete` methods
# =============================================================================================


@pytest.mark.parametrize('key, value, ttl', (
    ('key1', 128, None),
    ('key2', 'string value', 128),
    ('key3', None, 128),
    ('key3', User(name='Denis', age=666), -1),
))
def test_cache_get_set_delete(cache, key, value, ttl):
    """Test cache get/set/delete methods."""
    cache.autoclean = False

    # Initially no cached value
    found, cached_value = cache.get(key=key)
    assert not found

    # Set and get cached value
    cache_key = cache.set(key=key, value=value, ttl=ttl)
    found, cached_value = cache.get(key=key)
    assert found
    assert value == cached_value

    # Check TTL
    expected_ttl = ttl if ttl is not None else cache.default_ttl
    assert cache._get_cache_meta(cache_key).ttl == expected_ttl

    # Delete cached value
    assert cache.delete(key) == 1
    found, cached_value = cache.get(key=key)
    assert not found
    assert not cache._get_cache_meta(cache_key)


def test_cache_get_set_delete_type_error(cache):
    """Test TypeError on get/set/delete methods."""
    with pytest.raises(TypeError, match=r'.*Key must be string.*'):
        cache.get(key=CacheKey('my key'))

    with pytest.raises(TypeError, match=r'.*Key must be string.*'):
        cache.set(key=CacheKey('my key'), value=123)

    with pytest.raises(TypeError, match=r'.*Key must be string.*'):
        cache.delete(CacheKey('my key'))

# `_get` and `_set` methods
# =============================================================================================


def test_cache_private_set_without_meta(cache, sample_cache_key):
    """Test `_set` method without meta."""
    with pytest.raises(TypeError, match=r'.*Meta must be.*'):
        cache._set(key=sample_cache_key, value=1, meta=None)


def test_cache_private_get_set_delete_invalid_key_type(cache, sample_cache_meta):
    """Test `_set` method without meta."""
    with pytest.raises(TypeError, match=r'.*Key must be*'):
        cache._set(key='Key', value=1, meta=sample_cache_meta)

    with pytest.raises(TypeError, match=r'.*Key must be*'):
        cache._get(key='Key')

    with pytest.raises(TypeError, match=r'.*Key must be*'):
        cache._delete('Key', 'Another key')


def test_cache_private_get_set(cache, sample_cache_key, sample_cache_meta):
    """Test `_get` and `_set` methods."""
    # Cache miss
    found, value = cache._get(key=sample_cache_key)
    assert not found
    assert not value

    # Add cached value
    cache._set(key=sample_cache_key, value=123, meta=sample_cache_meta)

    # Cache hit!
    found, value = cache._get(key=sample_cache_key)
    assert found
    assert value == 123

    # Delete cached value
    assert cache._delete(sample_cache_key) == 1

    found, value = cache._get(key=sample_cache_key)
    assert not found


def test_cache_private_delete(cache, sample_cache_meta):
    """Test `_delete` method."""
    # Delete non-existing keys
    assert cache._delete(CacheKey('a__1'), CacheKey('b__1')) == 0

    # Add 1 value and delete again
    cache._set(key=CacheKey('a__1'), value=1, meta=sample_cache_meta)
    assert cache._delete(CacheKey('a__1'), CacheKey('b__1')) == 1
