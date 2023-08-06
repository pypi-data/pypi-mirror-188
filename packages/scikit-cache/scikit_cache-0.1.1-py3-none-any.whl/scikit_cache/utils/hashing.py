import inspect
import logging
from types import CodeType
from typing import (
    Any,
    Callable,
)

import joblib

from .base import get_func_name
from .estimators import (
    get_estimator_params,
    is_estimator,
)

logger = logging.getLogger('scikit_cache.hashing')


def hash_for_simple_object(obj: Any) -> str:
    """Get hash for any object."""
    return str(joblib.hash(obj))


def hash_for_none() -> str:
    """Get simple hash for None objects."""
    return '0' * 32


def hash_for_code(code: CodeType) -> str:
    """Get hash for ``code`` object."""
    if not isinstance(code, CodeType):
        raise TypeError(f'Parameter ``code`` must be ``CodeType``, not {type(code)}')

    try:
        co_consts_hash = hash_for_iterable(code.co_consts)
    except Exception as e:
        logger.warning(f'Error on hashing code consts {code}\n{e!r}')
        co_consts_hash = hash_for_simple_object(code.co_consts)

    return hash_for_simple_object(co_consts_hash.encode() + code.co_code)


def hash_for_iterable(iterable: Any) -> str:
    """Get hash for iterable objects."""
    return hash_for_simple_object(''.join(hash_by_type(value) for value in iterable))


def hash_for_dict(_dict: dict) -> str:
    """Get hash for dict objects."""
    if not isinstance(_dict, dict):
        raise TypeError(f'Parameter ``_dict`` must be dict, not {type(_dict)}')

    return hash_for_simple_object({k: hash_by_type(v) for k, v in _dict.items()})


def hash_for_callable(func: Callable, include_name: bool = True) -> str:
    """Hash for callable objects."""
    if not callable(func):
        raise TypeError(f'Parameter ``func`` must be callable, not {type(func)}')

    try:
        result = hash_for_code(func.__code__)
    except Exception as e:
        logger.warning(f'Error on hashing func code {func}\n{e!r}')
        result = hash_for_simple_object(func)

    if include_name:
        result = hash_for_simple_object(f'{result}.{get_func_name(func)}')

    return result


def hash_for_class(_class: type) -> str:
    """Get hash for ``class`` object.

    NOTE: It's poor hash implementation but works for some cases.
    """
    try:
        return hash_for_simple_object(inspect.getsource(_class))
    except Exception as e:
        logger.warning(f'Error on hashing class {_class}\n{e!r}')
        return hash_for_simple_object(_class)


def hash_for_estimator(obj: Any) -> str:
    """Get hash for ``sklearn.BaseEstimator`` instance."""
    estimator_class = obj.__class__
    estimator_params = get_estimator_params(obj, all_params=True)
    return hash_for_class(estimator_class) + hash_for_dict(estimator_params)


def hash_by_type(obj: Any) -> str:
    """Hash for any object depending on it's type."""
    if obj is None:
        return hash_for_none()
    elif isinstance(obj, (list, tuple, set)):
        return hash_for_iterable(obj)
    elif isinstance(obj, dict):
        return hash_for_dict(obj)
    elif is_estimator(obj):
        return hash_for_estimator(obj)
    elif isinstance(obj, (str, int, float, bytes, frozenset)):
        pass
    elif inspect.isclass(obj):
        return hash_for_class(obj)
    elif callable(obj):
        return hash_for_callable(obj)
    elif isinstance(obj, CodeType):
        return hash_for_code(obj)

    return hash_for_simple_object(obj)
