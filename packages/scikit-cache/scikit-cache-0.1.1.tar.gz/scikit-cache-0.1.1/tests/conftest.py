import pytest

from scikit_cache.components.file_handler import FileCacheHandler
from scikit_cache.controller import CacheController
from scikit_cache.resources import (
    CacheKey,
    ObjCacheMeta,
)
from scikit_cache.utils import (
    get_installed_packages,
    get_pickle_version,
    get_python_version,
    get_self_version,
)

TEST_CACHE_DIR = '.pytest_scikit_cache'


@pytest.fixture
def cache_dir():
    return TEST_CACHE_DIR


@pytest.fixture(scope='session')
def sample_cache_key():
    return CacheKey('test')


@pytest.fixture(scope='session')
def sample_cache_meta():
    return ObjCacheMeta(
        author='test',
        python_version=get_python_version(),
        pickle_version=get_pickle_version(),
        self_version=get_self_version(),
        installed_packages=get_installed_packages(),
        object_size=123,
        ttl=-1,
        func_name='sample_cache_meta',
        func_code_hash='sample_cache_meta',
        func_args_kwargs={'args': [], 'kwargs': {}},
    )


@pytest.fixture
def build_cache():
    """Fixture to build ``CacheController`` instance."""
    def wrapper(**kwargs):
        default_params = {
            'cache_dir': TEST_CACHE_DIR,
            'logger': None,
            'default_ttl': 3600,
            'autoclean': True,
        }
        return CacheController(**{**default_params, **kwargs})
    return wrapper


@pytest.fixture
def file_handler():
    handler = FileCacheHandler(TEST_CACHE_DIR)
    yield handler
    handler.wipe_cache_dir()


@pytest.fixture
def cache(build_cache):
    cache = build_cache()
    yield cache
    cache.disable()
    cache.wipe()
