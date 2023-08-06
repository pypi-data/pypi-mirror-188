import time

import pytest

from scikit_cache.components import cache_autoclean
from scikit_cache.resources import CacheKey


def test_cleanup_cache_by_ttl_without_autoclean(build_cache):
    """Test cleanup by TTL (autoclean=False)."""
    cache = build_cache(autoclean=False, default_ttl=360)

    keys_ttl = [None, -1, 0, 1, 128]
    expected_deleted = ['key_0', 'key_1']

    for ttl in keys_ttl:
        cache.set(key=f'key_{ttl}', value=f'value_{ttl}', ttl=ttl)

    time.sleep(1)
    cache.clean()

    for ttl in keys_ttl:
        raw_key = f'key_{ttl}'
        cache_key = CacheKey.from_raw_key(raw_key)

        found, value = cache.get(key=raw_key)
        if raw_key in expected_deleted:
            assert not found
            assert cache_key not in cache.__meta_cache__
        else:
            assert found
            assert value == f'value_{ttl}'
            assert cache_key in cache.__meta_cache__

    cache.wipe()


def test_cleanup_cache_by_ttl_with_autoclean(build_cache):
    """Test cleanup by TTL (autoclean=True)."""
    cache = build_cache(autoclean=True, default_ttl=360)

    keys_ttl = [None, -1, 0, 1, 128]
    expected_deleted = ['key_0', 'key_1']

    for ttl in keys_ttl:
        cache.set(key=f'key_{ttl}', value=f'value_{ttl}', ttl=ttl)

    time.sleep(1)

    for ttl in keys_ttl:
        raw_key = f'key_{ttl}'
        cache_key = CacheKey.from_raw_key(raw_key)

        found, value = cache.get(key=raw_key)
        if raw_key in expected_deleted:
            assert not found
            assert cache_key not in cache.__meta_cache__
        else:
            assert found
            assert value == f'value_{ttl}'
            assert cache_key in cache.__meta_cache__

    cache.wipe()


def test_cleanup_by_max_cached_objects_disabled(build_cache):
    """Test disabled ``max_cached_objects`` parameter."""
    cache = build_cache(autoclean=True, max_cached_objects=None)

    for i in range(10):
        cache.set(f'key_{i}', f'value_{i}')

    for i in range(10):
        assert cache.get(f'key_{i}')[0]  # found

    cache.wipe()


@pytest.mark.parametrize('max_cached_objects, total_objects', (
    (1, 3),
    (3, 10),
    (5, 5),
))
def test_cleanup_by_max_cached_objects_and_last_created(
    build_cache, max_cached_objects, total_objects,
):
    """Test ``max_cached_objects`` parameter (autoclean_mode="last_created")."""
    cache = build_cache(
        autoclean=True,
        autoclean_mode='last_created',
        max_cached_objects=max_cached_objects,
    )
    assert cache._clean_sorting_func == cache._get_creation_time_by_cache_key

    for i in range(total_objects):
        cache.set(f'key_{i}', f'value_{i}')

    for i in range(total_objects):
        found = cache.get(f'key_{i}')[0]
        assert found if (i >= total_objects - max_cached_objects) else not found

    cache.wipe()


def test_cleanup_by_max_cached_objects_and_last_used(build_cache):
    """Test ``max_cached_objects`` parameter (autoclean_mode="last_used")."""
    max_cached_objects = 3
    total_objects = 10

    cache = build_cache(
        autoclean=False,
        autoclean_mode='last_used',
        max_cached_objects=max_cached_objects,
    )
    assert cache._clean_sorting_func == cache._get_access_time_by_cache_key

    for i in range(total_objects):
        cache.set(f'key_{i}', f'value_{i}')

    used_keys = ['key_2', 'key_4', 'key_7']
    for key in used_keys:
        assert cache.get(key)[0]

    cache.clean()

    for i in range(total_objects):
        key = f'key_{i}'
        found = cache.get(key)[0]
        assert found if key in used_keys else not found

    cache.wipe()


@pytest.mark.parametrize('max_cache_dir_size, total_objects, expected_found', (
    (36, 5, 0),  # less than 37 bytes
    (37, 5, 1),  # == 37 bytes
    ('37 bytes', 5, 1),  # string repr
    ('1MB', 5, 5),  # too much memory
))
def test_cleanup_by_max_cache_dir_size_and_last_created(
    build_cache, max_cache_dir_size, total_objects, expected_found,
):
    """Test ``max_cache_dir_size`` parameter (autoclean_mode="last_created").

    NOTE: string "value_size_is_37_bytes" size is 37 bytes :)
    """
    cache = build_cache(
        autoclean=True,
        autoclean_mode='last_created',
        max_cache_dir_size=max_cache_dir_size,
    )
    assert cache._clean_sorting_func == cache._get_creation_time_by_cache_key

    for i in range(total_objects):
        cache.set(f'key_{i}', 'value_size_is_37_bytes')

    found_number = sum(cache.get(f'key_{i}')[0] for i in range(total_objects))
    assert found_number == expected_found

    cache.wipe()


def test_cleanup_by_max_cache_dir_size_and_last_used(build_cache):
    """Test ``max_cache_dir_size`` parameter (autoclean_mode="last_used")."""
    max_cache_dir_size = 37 * 3
    total_objects = 10

    cache = build_cache(
        autoclean=False,
        autoclean_mode='last_used',
        max_cache_dir_size=max_cache_dir_size,
    )
    assert cache._clean_sorting_func == cache._get_access_time_by_cache_key

    for i in range(total_objects):
        cache.set(f'key_{i}', 'value_size_is_37_bytes')

    used_keys = ['key_2', 'key_4', 'key_7']
    for key in used_keys:
        assert cache.get(key)[0]

    assert cache.clean() == 7

    for i in range(total_objects):
        key = f'key_{i}'
        found = cache.get(key)[0]
        assert found if key in used_keys else not found

    cache.wipe()


def test_cleanup_by_all_parameters(build_cache):
    """Test cleanup by all methods at once."""
    total_objects = 10

    cache = build_cache(
        autoclean=False,
        autoclean_mode='last_used',
        max_cache_dir_size='200 bytes',
        max_cached_objects=3,
    )

    for i in range(total_objects):
        ttl = (total_objects - i - 1) * 10  # last object will have TTL = 0
        cache.set(f'key_{i}', 'value_size_is_37_bytes', ttl=ttl)

    assert cache.clean() == 8

    remaining_keys = ['key_7', 'key_8']  # because key_9 will be deleted by TTL too

    for i in range(total_objects):
        key = f'key_{i}'
        found = cache.get(key)[0]
        assert found if key in remaining_keys else not found

    cache.wipe()


@pytest.mark.parametrize('parameter, value, deleted', (
    ('clean_objects_by_ttl', True, 1),
    ('clean_objects_by_ttl', False, 0),
    # NOTE: `deleted` include 1 extra deleted by TTL object
    ('max_cached_objects', None, 1),
    ('max_cached_objects', 3, 8),
    ('max_cached_objects', 10, 1),
    ('max_cache_dir_size', None, 1),
    ('max_cache_dir_size', '10 bytes', 10),
    ('max_cache_dir_size', '100 bytes', 9),
    ('max_cache_dir_size', '1KB', 1),
))
def test_cleanup_in_manual_mode(cache, parameter, value, deleted):
    cache.autoclean = False
    total_objects = 10

    for i in range(total_objects):
        ttl = (total_objects - i - 1) * 10  # last object will have TTL = 0
        cache.set(f'key_{i}', 'value_size_is_37_bytes', ttl=ttl)

    assert cache.clean(**{parameter: value}) == deleted


def test_invalid_autoclean_mode(cache):
    """Test invalid `autoclean_mode`."""
    cache.autoclean_mode = 'invalid'
    cache.set('key1', 'value_size_is_37_bytes', ttl=-1)
    cache.set('key2', 'value_size_is_37_bytes', ttl=-1)

    with pytest.raises(ValueError, match=r'.*autoclean_mode.*'):
        cache.clean(max_cached_objects=1)


def test_invalid_cache_autoclean():
    """Test that `cache_autoclean` can be applied only to cache method."""
    with pytest.raises(ValueError, match=r'.*can only be applied to.*'):
        @cache_autoclean
        def foo():
            pass
