import pytest

from scikit_cache.controller import CacheController
from tests.conftest import TEST_CACHE_DIR

# Samples
# =================================================================================================

cache = CacheController(cache_dir=TEST_CACHE_DIR, logger=None, autoclean=False)
call_stack: list = []


@cache.decorator()
def sample_func(a: int, b: int) -> int:
    """Sample function for testing."""
    call_stack.append('sample_func')
    return a + b


@cache.decorator(ignored_kwargs=['c'])
def sample_func_2(a: int, b: int, c: int) -> int:
    """Sample function for testing."""
    call_stack.append('sample_func_2')
    return a + b + c


@cache.decorator(fixed_hash='sample_func_3')
def sample_func_3(a: int, b: int) -> int:
    """Sample function for testing."""
    call_stack.append('sample_func_3')
    return a - b


@cache.decorator(external_packages=['cresco'])
def sample_func_4(a: int, b: int) -> int:
    """Sample function for testing."""
    call_stack.append('sample_func_4')
    return a * b


@cache.decorator()
def func_no_args_kwargs() -> int:
    """Decorate function without args and kwargs."""
    return 1


# Tests
# =================================================================================================

def test_cache_for_func_no_args_kwargs():
    """Test that decorator could not cache function that has no args/kwargs."""
    with pytest.raises(ValueError, match=r'.*Could not cache function that has no args/kwargs.*'):
        func_no_args_kwargs(use_cache=True)


def test_cache_decorator_with_disabled_cache():
    """Test `cache.decorator` when cache is disabled."""
    call_stack.clear()

    assert sample_func(1, 2) == 3
    assert sample_func(1, 2) == 3
    assert len(call_stack) == 2

    cache.disable()
    cache.wipe()


def test_cache_decorator_with_enabled_cache():
    """Test `cache.decorator` when cache is enabled."""
    call_stack.clear()
    cache.enable()

    assert sample_func(1, 2) == 3  # cache miss
    assert sample_func(1, 2) == 3  # cache hit
    assert len(call_stack) == 1

    assert sample_func(2, 1) == 3  # cache miss
    assert len(call_stack) == 2

    cache.disable()
    cache.wipe()


def test_cache_decorator_with_not_similar_meta():
    """Test `cache.decorator` if meta is not similar.

    Artificial test. No one should change meta cache directly!
    """
    call_stack.clear()
    cache.enable()

    assert sample_func(1, 2) == 3  # cache miss
    assert sample_func(1, 2) == 3  # cache hit
    assert len(call_stack) == 1

    meta = list(cache.__meta_cache__.values())[0]
    meta.python_version = '4.4.4'

    assert sample_func(1, 2) == 3  # cache miss
    assert len(call_stack) == 2

    cache.disable()
    cache.wipe()


def test_cache_decorator_with_empty_meta():
    """Test `cache.decorator` if meta is empty.

    Artificial test. No one should change meta cache directly!
    """
    call_stack.clear()
    cache.enable()

    assert sample_func(1, 2) == 3  # cache miss
    assert sample_func(1, 2) == 3  # cache hit
    assert len(call_stack) == 1

    key = list(cache.__meta_cache__.keys())[0]
    cache.__meta_cache__[key] = None

    assert sample_func(1, 2) == 3  # cache miss
    assert len(call_stack) == 2

    cache.disable()
    cache.wipe()


def test_cache_decorator_with_ignored_kwargs_using_args():
    """Test `cache.decorator` with ignored kwargs but using args."""
    call_stack.clear()
    cache.enable()

    assert sample_func_2(1, 2, 3) == 6  # cache miss
    assert sample_func_2(1, 2, 3) == 6  # cache hit
    assert len(call_stack) == 1

    assert sample_func_2(1, 2, 100) == 103  # cache miss
    assert len(call_stack) == 2

    cache.disable()
    cache.wipe()


def test_cache_decorator_with_ignored_kwargs_using_kwargs():
    """Test `cache.decorator` with ignored kwargs and using kwargs."""
    call_stack.clear()
    cache.enable()

    assert sample_func_2(a=1, b=2, c=3) == 6  # cache miss
    assert sample_func_2(a=1, b=2, c=3) == 6  # cache hit
    assert len(call_stack) == 1

    assert sample_func_2(a=1, b=2, c=100) == 6  # cache hit, even it's incorrect
    assert len(call_stack) == 1

    cache.disable()
    cache.wipe()


def test_cache_decorator_with_fixed_hash():
    """Test `cache.decorator` with fixed hash."""
    call_stack.clear()
    cache.enable()

    assert sample_func_3(3, 2) == 1  # cache miss
    assert sample_func_3(3, 2) == 1  # cache hit
    assert len(call_stack) == 1

    meta_dict = cache._get_all_cache_meta()
    assert len(meta_dict) == 1

    sample_func_3_meta = list(meta_dict.values())[0]
    assert sample_func_3_meta.func_code_hash == 'sample_func_3'  # fixed hash

    cache.disable()
    cache.wipe()


def test_cache_decorator_with_func_check_packages_and_specified_packages():
    """Test `cache.decorator` with packages.

    `sample_func_4` has external packages specified.
    """
    call_stack.clear()
    cache.enable()

    cache.check_external_packages = True
    cache.check_python_version = False
    cache.check_pickle_version = False

    assert sample_func_4(2, 3) == 6  # cache miss
    assert sample_func_4(2, 3) == 6  # cache hit
    assert len(call_stack) == 1

    cache.check_external_packages = False
    cache.check_python_version = True
    cache.check_pickle_version = True

    cache.disable()
    cache.wipe()


def test_cache_decorator_with_func_check_packages_without_specified_packages():
    """Test `cache.decorator` with packages.

    `sample_func` has no external packages specified.
    """
    call_stack.clear()
    cache.enable()

    cache.check_external_packages = True
    cache.check_python_version = False
    cache.check_pickle_version = False

    assert sample_func(2, 3) == 5  # cache miss
    assert sample_func(2, 3) == 5  # cache hit
    assert len(call_stack) == 1

    cache.check_external_packages = False
    cache.check_python_version = True
    cache.check_pickle_version = True

    cache.disable()
    cache.wipe()


def test_decorator_force_use_cache_with_disabled_cache():
    """Test `use_cache` parameter (cache is disabled)."""
    cache.wipe()
    call_stack.clear()

    assert sample_func_4(2, 3) == 6  # no cache
    assert len(call_stack) == 1

    assert sample_func_4(2, 3, use_cache=True) == 6  # cache miss
    assert len(call_stack) == 2

    assert sample_func_4(2, 3, use_cache=True) == 6  # cache hit
    assert len(call_stack) == 2

    assert sample_func_4(2, 3, use_cache=False) == 6  # no cache again
    assert len(call_stack) == 3

    cache.disable()
    cache.wipe()


def test_decorator_force_use_cache_with_enabled_cache():
    """Test `use_cache` parameter (cache is enabled)."""
    call_stack.clear()
    cache.enable()

    assert sample_func_4(2, 3) == 6  # cache miss
    assert len(call_stack) == 1

    assert sample_func_4(2, 3) == 6  # cache hit
    assert len(call_stack) == 1

    assert sample_func_4(2, 3, use_cache=True) == 6  # cache hit again
    assert len(call_stack) == 1

    assert sample_func_4(2, 3, use_cache=False) == 6  # cache ignored
    assert len(call_stack) == 2

    assert sample_func_4(2, 3) == 6  # cache hit again
    assert len(call_stack) == 2

    cache.disable()
    cache.wipe()


def test_cache_decorator_in_read_write_mode():
    """Test `cache.decorator` in read-write mode."""
    call_stack.clear()
    cache.enable(mode='rw')

    assert sample_func(1, 2) == 3  # cache miss
    assert sample_func(1, 2) == 3  # cache hit
    assert len(call_stack) == 1
    assert len(cache.info(display=False)) == 1

    assert sample_func(2, 1) == 3  # cache miss
    assert len(call_stack) == 2
    assert len(cache.info(display=False)) == 2

    cache.disable()
    cache.wipe()


def test_cache_decorator_in_read_only_mode():
    """Test `cache.decorator` in read-only mode."""
    call_stack.clear()
    cache.enable(mode='r')

    assert sample_func(1, 2) == 3  # cache miss
    assert sample_func(1, 2) == 3  # cache miss, because not cache written
    assert len(call_stack) == 2
    assert len(cache.info(display=False)) == 0

    cache.enable(mode='rw')
    assert sample_func(1, 2) == 3  # cache miss, but cache added
    assert len(call_stack) == 3
    assert len(cache.info(display=False)) == 1

    cache.enable(mode='r')
    assert sample_func(1, 2) == 3  # cache hit
    assert len(call_stack) == 3
    assert len(cache.info(display=False)) == 1

    assert sample_func(2, 3) == 5  # cache miss
    assert len(call_stack) == 4
    assert len(cache.info(display=False)) == 1  # no cache added

    cache.disable()
    cache.wipe()


def test_cache_decorator_in_write_only_mode():
    """Test `cache.decorator` in write-only mode.

    Very strange mode, indeed :)
    """
    call_stack.clear()
    cache.enable(mode='w')

    assert sample_func(1, 2) == 3  # cache miss
    assert sample_func(1, 2) == 3  # cache miss
    assert len(call_stack) == 2
    assert len(cache.info(display=False)) == 2

    cache.disable()
    cache.wipe()
