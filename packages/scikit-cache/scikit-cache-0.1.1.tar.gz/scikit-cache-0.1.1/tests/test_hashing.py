import sys

import pytest
from sklearn.linear_model import LinearRegression

from scikit_cache.utils import hashing

# Samples
# =============================================================================================


def sample_func():
    return None


class SampleClass:
    pass

# Tests
# =============================================================================================


@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_simple_object():
    assert hashing.hash_for_simple_object('Any string') == 'bb878b4e9b85f34f77ac48346e097d6a'


def test_hash_for_none():
    assert hashing.hash_for_none() == '0' * 32


@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_code():
    assert hashing.hash_for_code(sample_func.__code__) == '4d4bbbac2eb7527664db2aa770f32b8e'


def test_hash_for_code_type_error():
    with pytest.raises(TypeError, match=r'.*CodeType.*'):
        hashing.hash_for_code(1)


@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_code_exception(mocker):
    mocked = mocker.patch.object(hashing, 'hash_for_iterable')
    mocked.side_effect = ValueError
    assert hashing.hash_for_code(sample_func.__code__) == '2356b3dc164884f4c8ad4fd26c59b46e'


@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_iterable():
    assert hashing.hash_for_iterable([1, 2, 3]) == '5985cc486e8d6df98a47dc0bbadfa609'


@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_dict():
    assert hashing.hash_for_dict({'1': None}) == '7a16b5d6fdafefa858cbce0921a209b7'


def test_hash_for_dict_type_error():
    with pytest.raises(TypeError, match=r'.*must be dict.*'):
        hashing.hash_for_dict([])


@pytest.mark.parametrize('include_name, expected', (
    (True, 'e9898445604b4fddbc8d580e31f82eec'),
    (False, '4d4bbbac2eb7527664db2aa770f32b8e'),
))
@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_callable(include_name, expected):
    assert hashing.hash_for_callable(sample_func, include_name) == expected


def test_hash_for_callable_type_error():
    with pytest.raises(TypeError, match=r'.*must be callable.*'):
        hashing.hash_for_callable(1)


@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_callable_exception(mocker):
    mocked = mocker.patch.object(hashing, 'hash_for_code')
    mocked.side_effect = ValueError

    assert hashing.hash_for_callable(sample_func) == '5a489c5a8e5960f1a19420c3ddedd4e8'


@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_class():
    assert hashing.hash_for_class(SampleClass) == 'ae1a13c159028324849574ae3315fadc'


@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_class_exception():
    assert hashing.hash_for_class(1) == '366da3d0fc5e8ed36f9eac8083a46ae8'


@pytest.mark.parametrize('value, expected', (
    (
        LinearRegression(),
        '9808f07244881dd9f242f4e745eebdc2f71e8e5c834a789f1825e011a4722f70',
    ),
    (
        LinearRegression(positive=True),
        '9808f07244881dd9f242f4e745eebdc2f0f6702972d55f098d306a634da0f3fa',
    ),
))
@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_for_estimator(value, expected):
    assert hashing.hash_for_estimator(value) == expected


@pytest.mark.parametrize('value, expected', (
    (None, '0' * 32),
    ('Any string', 'bb878b4e9b85f34f77ac48346e097d6a'),
    (sample_func.__code__, '4d4bbbac2eb7527664db2aa770f32b8e'),
    ([1, 2, 3], '5985cc486e8d6df98a47dc0bbadfa609'),
    ({'1': None}, '7a16b5d6fdafefa858cbce0921a209b7'),
    (sample_func, 'e9898445604b4fddbc8d580e31f82eec'),
    (SampleClass, 'ae1a13c159028324849574ae3315fadc'),
    (SampleClass(), '296308d9745d39bbe303ef1c3d1f09d8'),
    (LinearRegression(), '9808f07244881dd9f242f4e745eebdc2f71e8e5c834a789f1825e011a4722f70'),
))
@pytest.mark.skipif(sys.version_info > (3, 8), reason='hashes actual for python3.8 only')
def test_hash_by_type(value, expected):
    assert hashing.hash_by_type(value) == expected
