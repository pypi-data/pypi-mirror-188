import logging
import shutil

import pytest

from scikit_cache.controller import CacheController
from scikit_cache.resources import CacheKey

# Samples
# =============================================================================================


def func_a():
    """Sample func a."""


def func_b():
    """Sample func a."""


def func_c():
    """Sample func a."""

# Tests
# =============================================================================================


def test_controller_invalid_params(cache_dir):
    """Test init cache controller with invalid/missing params."""
    with pytest.raises(ValueError):
        CacheController(cache_dir=cache_dir, check_python_version='Invalid')


@pytest.mark.parametrize('cache_only, cache_exclude, success', (
    (None, None, True),  # no white/black lists
    ([func_a, func_b, func_c], None, True),  # whitelist hit
    ([func_b, func_c], None, False),  # whitelist miss
    (None, [func_b, func_c], True),  # blacklist miss
    (None, [func_a, func_b, func_c], False),  # blacklist hit
))
def test_controller_is_enabled_for_func(cache, cache_only, cache_exclude, success):
    """Test `is_enabled_for_func` method.

    NOTE: whitelist is prior to blacklist in order of checks.
    """
    cache.enable(only_functions=cache_only, exclude_functions=cache_exclude)
    assert cache.is_enabled_for_func(func=func_a) is success
    assert cache.is_enabled_for_any


def test_controller_enable_with_invalid_params(cache):
    """Test `enable` method with invalid params."""
    with pytest.raises(ValueError, match=r'Specify.*'):
        cache.enable(only_functions=[func_a], exclude_functions=[func_b])

    with pytest.raises(ValueError, match=r'.*callable.*'):
        cache.enable(only_functions=['func_a'])


def test_controller_get_cache_meta(cache, sample_cache_key, sample_cache_meta):
    """Test `_get_cache_meta` method."""
    # meta not found
    assert not cache._get_cache_meta(key=sample_cache_key)
    assert not cache._get_all_cache_meta()

    # check that even None is saved to internal cache too
    assert cache.__meta_cache__ == {sample_cache_key: None}
    assert not cache._get_all_cache_meta()

    # invalidate internal cache
    cache._invalidate_internal_cache(sample_cache_key)
    assert not cache.__meta_cache__
    assert not cache._get_all_cache_meta()

    # add cached value
    cache._set(
        key=sample_cache_key,
        value=1,
        meta=sample_cache_meta,
    )

    # meta found
    new_meta = cache._get_cache_meta(key=sample_cache_key)
    assert new_meta.func_code_hash == 'sample_cache_meta'
    assert cache.__meta_cache__[sample_cache_key] == new_meta
    assert len(cache._get_all_cache_meta()) == 1

    # cache hit
    new_meta = cache._get_cache_meta(key=sample_cache_key)
    assert new_meta.func_code_hash == 'sample_cache_meta'
    assert cache.__meta_cache__[sample_cache_key] == new_meta
    assert len(cache._get_all_cache_meta()) == 1


def test_controller_internal_cache(cache, cache_dir, sample_cache_meta):
    """Test `_init_internal_cache` and `_invalidate_internal_cache` methods."""
    cache_keys = [CacheKey(k) for k in ('test__1', 'test__2', 'test__3', 'test__4')]
    parent_key = CacheKey('test')
    for key in cache_keys:
        cache._set(
            key=key,
            value=key * 10,
            meta=sample_cache_meta,
        )

    new_cache_ctrl = CacheController(cache_dir=cache_dir)
    assert len(new_cache_ctrl.__meta_cache__) == len(cache_keys)
    assert sorted(new_cache_ctrl.__child_keys_cache__.keys()) == [parent_key] + cache_keys

    # Check that key is in cache with its parent
    t3_key = CacheKey('test__3')
    assert t3_key in new_cache_ctrl.__meta_cache__
    assert t3_key in new_cache_ctrl.__child_keys_cache__
    assert parent_key not in new_cache_ctrl.__meta_cache__
    assert parent_key in new_cache_ctrl.__child_keys_cache__

    # invalidate key with its parent key
    assert new_cache_ctrl._invalidate_internal_cache(t3_key) == 2  # `test__3` + `test`

    # Check that key is no longer in cache with its parent
    assert t3_key not in new_cache_ctrl.__meta_cache__
    assert t3_key not in new_cache_ctrl.__child_keys_cache__

    assert parent_key not in new_cache_ctrl.__meta_cache__
    assert parent_key not in new_cache_ctrl.__child_keys_cache__

    # Get child keys for parent key and check that cache is updated
    assert len(new_cache_ctrl._find_child_keys(parent_key)) == 4
    assert parent_key in new_cache_ctrl.__child_keys_cache__

    # Invalidate all keys
    assert new_cache_ctrl._invalidate_internal_cache(clear_all=True) == 3
    assert not new_cache_ctrl.__meta_cache__
    assert not new_cache_ctrl.__child_keys_cache__


def test_controller_log_using_print(cache_dir):
    """Test `log` method using print."""
    cache_ctrl = CacheController(cache_dir=cache_dir, logger='print')
    cache_ctrl._log('OK')


def test_controller_log_using_invalid_logger(cache_dir):
    """Test `log` method using print."""
    cache_ctrl = CacheController(cache_dir=cache_dir)
    cache_ctrl.logger = 'InvalidLogger'
    with pytest.raises(TypeError, match=r'.*Unknown logger type.*'):
        cache_ctrl._log('OK')


def test_controller_log_using_logger(cache_dir, mocker):
    """Test `log` method using built-in logging."""
    logger = logging.getLogger(__name__)
    mocked_info = mocker.patch.object(logger, 'info')

    cache_ctrl = CacheController(cache_dir=cache_dir, logger='logger')
    cache_ctrl._log('Hello World', logger=logger)
    mocked_info.assert_called_once()


def test_controller_cache_info_success(cache, sample_cache_key, sample_cache_meta):
    """Test `cache_info` function."""
    messages = []

    def suppressed_print(msg):
        messages.append(msg)

    assert not cache.info(display=False)

    cache.info(display=suppressed_print)
    assert len(messages) == 3
    assert messages[1] == 'Keys: 0'

    # add cached value (for func)
    cache._set(
        key=sample_cache_key,
        value=1,
        meta=sample_cache_meta,
    )
    # add cached value (raw key)
    cache.set(key='raw key', value=2)

    # invalidate and warm internal cache
    cache._init_internal_cache(invalidate_first=True)

    found_info = cache.info(display=False)
    assert found_info[str(sample_cache_key)]

    # stats only output
    messages.clear()
    cache.info(display=suppressed_print)
    assert len(messages) == 3

    # with keys
    messages.clear()
    cache.info(display=suppressed_print, keys=True)
    assert len(messages) == 9

    # with keys and without stats
    messages.clear()
    cache.info(display=suppressed_print, keys=True, show_total=False)
    assert len(messages) == 6

    # full output
    messages.clear()
    cache.info(display=suppressed_print, keys=True, full=True)
    assert len(messages) == 20

    # full output without packages
    messages.clear()
    cache.info(display=suppressed_print, keys=True, full=True, show_packages=False)
    assert len(messages) == 18


def test_cache_repr(cache):
    """Test `__repr__` method."""
    assert repr(cache)


def test_cache_mode(cache):
    """Test `mode` property."""
    assert cache.mode == 'rw'


def test_cache_keys(cache):
    """Test `keys()` method."""
    assert cache.keys() == []

    cache.set(key='1', value='2')
    assert len(cache.keys()) == 1


def test_cache_controller_with_invalid_mode(cache):
    """Test invalid mode for cache."""
    with pytest.raises(ValueError, match=r'.*Unknown mode.*'):
        cache.enable(mode='xr')


def test_change_cache_dir(cache):
    """Test that cache dir change will invalidate internal cache."""
    old_cache_dir = cache.cache_dir
    new_cache_dir = '.new_cache_dir'

    cache.max_cache_dir_size = '1MB'
    cache.set(key='1', value='2')
    assert cache.__meta_cache__

    cache.cache_dir = new_cache_dir
    assert not cache.__meta_cache__

    cache.clean()

    shutil.rmtree(old_cache_dir, ignore_errors=True)
