import pytest
from pydantic import BaseModel

from scikit_cache.resources import CacheKey


class User(BaseModel):
    name: str
    age: int

# `get`, `set`, `delete` methods
# =============================================================================================


@pytest.mark.parametrize('key, value, ttl', (
    (CacheKey('key1'), 128, 0),
    (CacheKey('key2'), 'string value', 128),
    (CacheKey('key3'), None, 128),
    (CacheKey('key3'), User(name='Denis', age=666), -1),
))
def test_handler_get_set_delete(file_handler, sample_cache_meta, key, value, ttl):
    """Test handler get/set/delete methods."""
    sample_cache_meta.ttl = ttl
    # Initially no cached value
    found, cached_value = file_handler.get(key=key)
    assert not found

    # Set and get cached value
    file_handler.set(key=key, value=value, meta=sample_cache_meta)
    found, cached_value = file_handler.get(key=key)
    assert found
    assert value == cached_value

    # Check TTL
    assert file_handler.get_cache_meta(key).ttl == ttl

    # Delete cached value
    assert file_handler.delete(key) == 1
    found, cached_value = file_handler.get(key=key)
    assert not found
    assert not file_handler.get_cache_meta(key)


def test_cache_get_set_delete_type_error(file_handler):
    """Test TypeError on get/set/delete methods."""
    with pytest.raises(TypeError, match=r'.*Key must be.*'):
        file_handler.get(key='my key')

    with pytest.raises(TypeError, match=r'.*Key must be.*'):
        file_handler.set(key='my key', value=None, meta=None)

    with pytest.raises(TypeError, match=r'.*Key must be.*'):
        file_handler.delete('my key')
