import pytest

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


def test_cache_key_magic_methods(sample_cache_key):
    """Test ``CacheKey`` magic methods."""
    assert str(sample_cache_key) == sample_cache_key
    assert repr(sample_cache_key) == f'<CacheKey: {sample_cache_key}>'


@pytest.mark.parametrize('raw_value, expected', (
    ('a__b__c', 'a/b/c'),
    ('__root__', ''),
    ('', ValueError),
))
def test_cache_key_as_filepath(raw_value, expected):
    """Test ``CacheKey`` as filepath."""
    key = CacheKey(raw_value)

    if expected is ValueError:
        with pytest.raises(ValueError):
            key.as_filepath
    else:
        assert key.as_filepath == expected


@pytest.mark.parametrize('raw_value, include_self, expected', (
    ('a', True, ['a']),
    ('a', False, []),
    ('a__b__c', True, ['a', 'a__b', 'a__b__c']),
    ('a__b__c', False, ['a', 'a__b']),
))
def test_cache_key_get_parent_keys(raw_value, include_self, expected):
    """Test ``CacheKey.get_parent_keys`` method."""
    assert CacheKey(raw_value).get_parent_keys(include_self=include_self) == expected


@pytest.mark.parametrize('cache_meta_1, cache_meta_2, version_check_params, is_similar', (
    ({}, {}, {}, True),
    # python versions
    (
        {'python_version': '3.7.9'},
        {'python_version': '2.7.1'},
        {'check_python_version': False},
        True,
    ),
    (
        {'python_version': '3.7.9'},
        {'python_version': '3.10.1'},
        {'check_python_version': True, 'check_version_level': 1},
        True,
    ),
    (
        {'python_version': '3.7.9'},
        {'python_version': '3.10.1'},
        {'check_python_version': True, 'check_version_level': 2},
        False,
    ),
    (
        {'python_version': '3.7.9'},
        {'python_version': '3.10.1'},
        {'check_python_version': True, 'check_version_level': 5},
        False,
    ),
    (
        {'python_version': '3.8.1'},
        {'python_version': '3.8.1'},
        {'check_python_version': True, 'check_version_level': 5},
        True,
    ),
    # pickle versions
    (
        {'pickle_version': '3.0.0'},
        {'pickle_version': '4.0.0'},
        {'check_pickle_version': False},
        True,
    ),
    (
        {'pickle_version': '3.0.0'},
        {'pickle_version': '4.0.0'},
        {'check_pickle_version': True},
        False,
    ),
    (
        {'pickle_version': '4.0.1'},
        {'pickle_version': '4.0.3'},
        {'check_pickle_version': True},
        True,
    ),
    # self versions
    (
        {'self_version': '3.0.0'},
        {'self_version': '4.0.0'},
        {'check_self_version': False},
        True,
    ),
    (
        {'self_version': '3.0.0'},
        {'self_version': '4.0.0'},
        {'check_self_version': True},
        False,
    ),
    (
        {'self_version': '4.0.1'},
        {'self_version': '4.0.3'},
        {'check_self_version': True},
        True,
    ),
    # func hash
    (
        {'func_code_hash': 'asd8asd9ajsdlkajsd98asdka'},
        {'func_code_hash': 'gffdkjfdj1212bsad7asdakad'},
        {'check_func_source': False},
        True,
    ),
    (
        {'func_code_hash': 'asd8asd9ajsdlkajsd98asdka'},
        {'func_code_hash': 'gffdkjfdj1212bsad7asdakad'},
        {'check_func_source': True},
        False,
    ),
    (
        {'func_code_hash': 'asd8asd9ajsdlkajsd98asdka'},
        {'func_code_hash': 'asd8asd9ajsdlkajsd98asdka'},
        {'check_func_source': True},
        True,
    ),
    # check packages
    (
        {'installed_packages': {'a': '0.0.0'}},
        {'installed_packages': {'a': '1.0.0'}},
        {'check_external_packages': False},
        True,
    ),
    (
        {'installed_packages': {'a': '0.0.0'}},
        {'installed_packages': {'a': '1.0.0'}},
        {'check_external_packages': True},
        False,
    ),
    (
        {'installed_packages': {'a': '0.0.1'}},
        {'installed_packages': {'a': '0.0.2'}},
        {'check_external_packages': True},
        True,
    ),
    (
        {'installed_packages': {'a': '0.0.1', 'b': '0.0.0'}},
        {'installed_packages': {'a': '0.0.2', 'c': '1.0.0'}},
        {'check_external_packages': True},
        True,
    ),
    (
        {'installed_packages': {'a': '0.0.1', 'b': '0.0.0'}},
        {'installed_packages': {'a': '0.0.2', 'b': '1.0.0'}},
        {'check_external_packages': ['a']},
        True,
    ),
    (
        {'installed_packages': {'a': '0.0.1', 'b': '0.0.0'}},
        {'installed_packages': {'a': '0.0.2', 'b': '1.0.0'}},
        {'check_external_packages': ['a', 'b']},
        False,
    ),
    (
        {'installed_packages': {'a': '0.0.1', 'b': '0.0.0'}},
        {'installed_packages': {'a': '0.0.2', 'b': '1.0.0'}},
        {'check_external_packages': ['c', 'd']},
        True,
    ),
))
def test_cache_meta_is_similar(cache_meta_1, cache_meta_2, version_check_params, is_similar):
    """Test ``ObjCacheMeta.is_similar`` method."""
    default_meta_params = {
        'author': 'test',
        'ttl': 0,
        'object_size': 0,
        'func_code_hash': '12345',
        'func_name': 'test',
        'func_args_kwargs': {'args': [1], 'kwargs': {}},
        'python_version': get_python_version(),
        'pickle_version': get_pickle_version(),
        'self_version': get_self_version(),
        'installed_packages': get_installed_packages(),
    }
    default_version_check_params = {
        'check_version_level': 2,
        'check_python_version': True,
        'check_pickle_version': True,
        'check_external_packages': False,
        'check_func_source': True,
    }

    cache_meta_1 = ObjCacheMeta(**{**default_meta_params, **cache_meta_1})
    cache_meta_2 = ObjCacheMeta(**{**default_meta_params, **cache_meta_2})
    version_check_params = {**default_version_check_params, **version_check_params}
    assert cache_meta_1.is_similar_to(cache_meta_2, **version_check_params) is is_similar


@pytest.mark.parametrize('value, expected', (
    ('x' * 10, 'x' * 10),
    ('x' * 50, 'x' * 50),
    ('x' * 100, 'x' * 50 + ' (len = 100)'),
))
def test_raw_key_length_validator(value, expected):
    """Test `raw_key_length_validator`."""
    default_meta_params = {
        'author': 'test',
        'ttl': 0,
        'object_size': 0,
        'func_code_hash': '12345',
        'func_name': 'test',
        'func_args_kwargs': {'args': [1], 'kwargs': {}},
        'python_version': get_python_version(),
        'pickle_version': get_pickle_version(),
        'self_version': get_self_version(),
        'installed_packages': get_installed_packages(),
    }
    meta = ObjCacheMeta(raw_key=value, **default_meta_params)
    assert meta.raw_key == expected


def test_meta_str_and_repr(sample_cache_meta):
    """Test ``ObjCacheMeta`` repr."""
    assert repr(sample_cache_meta) == str(sample_cache_meta)


def test_meta_from_raw_key_type_error(cache):
    """Test type error on `ObjCacheMeta.from_raw_key`."""
    with pytest.raises(TypeError, match=r'.*Key must be string.*'):
        ObjCacheMeta.from_raw_key(raw_key=CacheKey('123'), ttl=-1, base_meta=cache._base_meta)
