from scikit_cache.resources import (
    BaseCacheMeta,
    CacheKey,
    ObjCacheMeta,
)


def sample_func(a: int, b: int) -> int:
    """Sample function for testing."""
    return a + b


def sample_func_2(a: int, b: int) -> int:
    """Sample function for testing."""
    return a - b


# Tests
# ========================================================================


def test_func_cache_set_success(cache):
    """Test `_func_cache_set` success."""
    key, meta = cache._build_key_meta(func=sample_func, func_args=(1, 2), func_kwargs={})
    new_key, new_meta = cache._func_cache_set(key, meta, func_result=1)

    assert len(new_key) > len(key)
    assert meta is new_meta

    current_module = test_func_cache_set_success.__module__
    assert f'{current_module}.sample_func' in new_key
    assert len(new_key.get_parent_keys()) == 3


def test_func_cache_get_success(cache):
    """Test `_func_cache_get` success."""
    key, meta = cache._build_key_meta(func=sample_func, func_args=(1, 2), func_kwargs={})

    # Cache miss
    found, value = cache._func_cache_get(key, meta)
    assert not found
    assert not value

    # Add cached value
    assert cache._func_cache_set(key, meta, func_result=123)

    # Cache hit!
    found, value = cache._func_cache_get(key, meta)
    assert found
    assert value == 123


def test_func_cache_get_with_other_cached_values(cache):
    """Test `func_cache_get` when cache exists for other variations of same function."""
    key, meta = cache._build_key_meta(func=sample_func, func_args=(1, 2), func_kwargs={})
    key_2, meta_2 = cache._build_key_meta(func=sample_func, func_args=(2, 3), func_kwargs={})
    key_3, meta_3 = cache._build_key_meta(func=sample_func_2, func_args=(1, 2), func_kwargs={})

    # Cache miss
    assert not cache._func_cache_get(key, meta)[0]

    # Add cached value for same function but other arguments
    assert cache._func_cache_set(key_2, meta_2, func_result=123)

    # Add cached value for another function but same arguments
    assert cache._func_cache_set(key_3, meta_3, func_result=123)

    # Add cached value for same function and same arguments, but different python version
    cache_key = CacheKey.from_func(
        func=sample_func,
        func_args=(1, 2),
        func_kwargs=None,
    )
    cache_meta = ObjCacheMeta.from_func(
        func=sample_func,
        func_args=(1, 2),
        func_kwargs=None,
        fixed_hash=None,
        func_ttl=-1,
        base_meta=BaseCacheMeta(
            author='test',
            python_version='0.0.0',
            pickle_version='0.0.0',
            self_version='0.0.0',
            installed_packages=[],
        ),
    )
    cache._set(
        key=cache_key,
        value=123,
        meta=cache_meta,
    )

    # Cache miss again
    assert not cache._func_cache_get(key, meta)[0]
