import os
from datetime import datetime

import pandas as pd
import pytest

from scikit_cache.controller import CacheController
from scikit_cache.utils import (
    color_msg,
    format_bytes_to_str,
    format_str_to_bytes,
    get_datetime_str,
    get_file_access_time,
    get_func_name,
    get_random_hex,
    get_username,
    is_scikit_cache_hit,
    set_file_access_time,
    yaml_repr,
)


def test_get_datetime_str():
    """Test `get_datetime_str`."""
    assert datetime.fromisoformat(get_datetime_str())


@pytest.mark.parametrize('bits, expected', (
    (32, 8),
    (128, 32),
    (256, 64),
))
def test_get_random_hex(bits, expected):
    """Test `get_random_hex`.

    Function has varying result length.
    """
    value_len = len(get_random_hex(bits=bits))
    assert (expected - 1) <= value_len <= (expected + 1)


def test_get_func_name():
    """Test `get_func_name`."""
    assert get_func_name(test_get_func_name) == 'test_utils.test_get_func_name'


@pytest.mark.parametrize('value, expected', (
    (pd.DataFrame(), '<DataFrame: (0, 0)>'),
    (1, 1),
    (2.3, 2.3),
    ('hello', 'hello'),
    (b'hello', "b'hello'"),
    ([1, 2, 3], [1, 2, 3]),
    ((1, 2, 3), [1, 2, 3]),
    ({'k': 'v'}, {'k': 'v'}),
    ({'k': b'hello'}, {'k': "b'hello'"}),
))
def test_yaml_repr(value, expected):
    """Test `yaml_repr`."""
    assert yaml_repr(value) == expected


@pytest.mark.parametrize('value, expected', (
    (100, '100 bytes'),
    (1000, '1000 bytes'),
    (2048, '2KB'),
    (1048576, '1MB'),
    (10485760, '10MB'),
))
def test_format_bytes_to_str(value, expected):
    """Test `format_bytes_to_str`."""
    assert format_bytes_to_str(value) == expected


@pytest.mark.parametrize('value, expected', (
    ('100 bytes', 100),
    ('1000 bytes', 1000),
    ('123456789 bytes', 123456789),
    ('1 KB', 1024),
    ('1KB', 1024),
    ('1MB', 1048576),
    ('1GB', 1073741824),
    ('1EB', 1152921504606846976),
))
def test_format_str_to_bytes(value, expected):
    """Test `format_str_to_bytes`."""
    assert format_str_to_bytes(value) == expected


def test_test_format_str_to_bytes_value_error():
    """Test `format_str_to_bytes` with invalid value."""
    with pytest.raises(ValueError, match=r'.*No units found in string.*'):
        format_str_to_bytes('123 XB')


def test_get_username(mocker):
    """Test `get_username`."""
    assert get_username()

    mocked = mocker.patch.object(os, 'getuid')
    mocked.return_value = '123'  # to raise Exception

    assert get_username()


def test_file_access_time():
    """Test `get_file_access_time` and `set_file_access_time`."""
    file_path = '.test_file_access_time'
    with open(file_path, 'w') as f:
        f.write('Hello')

    assert isinstance(get_file_access_time(file_path), float)

    st_atime = set_file_access_time(file_path, atime='now')
    assert get_file_access_time(file_path) == st_atime

    some_datetime = datetime.fromisoformat('2022-09-06T21:27:41.882663')
    st_atime = set_file_access_time(file_path, atime=some_datetime)
    assert get_file_access_time(file_path) == some_datetime.timestamp() == st_atime

    os.remove(file_path)


@pytest.mark.parametrize('msg, color', (
    ('msg', None),
    ('msg', 'red'),
    ('msg', 'green'),
    ('msg', 'blue'),
    ('msg', 'yellow'),
))
def test_color_msg(msg, color):
    """Test `color_msg`."""
    assert isinstance(color_msg(msg, color), str)


def test_is_scikit_cache_hit(cache_dir):
    cache_ctrl = CacheController(cache_dir=cache_dir, logger='print')
    cache_ctrl.wipe()

    def nondecorated():
        return 1

    @cache_ctrl.decorator()
    def decorated(a: int):
        return a + 1

    # test for non-decorated func
    assert is_scikit_cache_hit(nondecorated) is None

    # decorated func with disabled cache
    decorated(2)
    assert is_scikit_cache_hit(decorated) is None

    # Enabled caching for func
    cache_ctrl.enable(cache_functions=True)

    # cache miss on first call
    decorated(2)
    assert is_scikit_cache_hit(decorated) is False

    # cache hit on second call
    decorated(2)
    assert is_scikit_cache_hit(decorated) is True

    cache_ctrl.wipe()
