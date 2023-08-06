import os
import pwd
import random
from datetime import datetime
from typing import (
    Any,
    Callable,
    Tuple,
)

SIZE_UNITS = (' bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB')
CACHE_HIT_ATTR = '__scikit_cache_hit__'


def is_scikit_cache_hit(func: Callable) -> Any:
    """Get saved attribute if where is cache hit or not.

    This CACHE_HIT_ATTR automatically added in ``DecoratorMixin`` to function dictionary and
    allows to detect cache hit/miss after function call.
    """
    if hasattr(func, '__wrapped__'):
        func = func.__wrapped__  # Extract original func from decorated

    return getattr(func, CACHE_HIT_ATTR, None)


def get_datetime_str() -> str:
    """Get datetime as string is ISO format."""
    return datetime.now().isoformat()


def get_random_hex(bits: int = 128) -> str:
    """Get random HEX string."""
    return '{0:x}'.format(random.getrandbits(bits))


def get_func_name(func: Callable) -> str:
    """Get full function name (with module path)."""
    try:
        return f'{func.__module__}.{func.__name__}'.replace('__', '')
    except AttributeError:
        raise ValueError(f'``get_func_name`` accepts callable objects, not {type(func)}')


def yaml_repr(value: Any) -> Any:
    """Represent value for YAML format."""
    # Pandas ``DataFrame`` or ``Series``
    if hasattr(value, 'shape'):
        return f'<{value.__class__.__name__}: {value.shape}>'

    # List/tuple
    if isinstance(value, (list, tuple)):
        return [yaml_repr(v) for v in value]

    # Dict
    if isinstance(value, dict):
        return {yaml_repr(k): yaml_repr(v) for k, v in value.items()}

    # YAML supported native types
    if isinstance(value, (int, float, bool, str)) or value is None:
        return value

    # All other objects
    return repr(value)


def get_username() -> str:
    """Get current username."""
    try:
        return pwd.getpwuid(os.getuid())[0]
    except Exception:
        return os.path.expanduser('~').split('/')[-1]


def format_bytes_to_str(
    size: int,
    units: Tuple[str, ...] = SIZE_UNITS,
) -> str:
    """Get human readable string representation of size in bytes."""
    return str(size) + units[0] if size < 1024 else format_bytes_to_str(size >> 10, units[1:])


def format_str_to_bytes(size: str) -> int:
    """Convert human readable strinb representaion of file size to integer.

    For example:
        >>> format_str_to_bytes(size='1 MB')
        1048576
    """
    size_multiplier = 1
    for i, unit in enumerate(SIZE_UNITS):
        if unit in size:
            size_part, _ = size.split(unit)
            size_multiplier = pow(1024, i) or 1
            return int(float(size_part.strip()) * size_multiplier)

    raise ValueError(f'No units found in string. Available units: {SIZE_UNITS}')
