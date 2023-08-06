from datetime import (
    datetime,
    timedelta,
)
from functools import wraps
from typing import (
    Any,
    Callable,
    List,
    TypeVar,
    Union,
    cast,
)

from scikit_cache.utils import (
    format_str_to_bytes,
    get_file_access_time,
)

from ..resources import CacheKey

F = TypeVar('F', bound=Callable[..., Any])


class CleanUpMixin:
    """Mixin for ``CacheController`` class with cleanup private methods."""

    def _get_clean_objects_by_expired_tl(self) -> List[CacheKey]:
        """Get list of cache keys with expired TTL."""
        current_time = datetime.now()
        expired_keys = []

        for cache_key, meta_cache in self._get_all_cache_meta().items():
            if meta_cache.ttl >= 0:
                creation_time = datetime.fromisoformat(meta_cache.creation_time)
                expire_time = creation_time + timedelta(seconds=meta_cache.ttl)
                if current_time > expire_time:
                    expired_keys.append(cache_key)

        return expired_keys

    def _get_clean_objects_by_max_number(self, max_number: int) -> List[CacheKey]:
        """Get list of cache keys to delete that exceed max number of objects."""
        meta_dict = self._get_all_cache_meta()
        delete_number = len(meta_dict) - max_number
        if delete_number < 1:
            return []

        return sorted(meta_dict, key=self._clean_sorting_func)[:delete_number]

    def _get_clean_objects_by_max_size(self, max_size: Union[int, str]) -> List[CacheKey]:
        """Get list of cache keys to delete that exceed max cache dir size."""
        if not isinstance(max_size, int):
            max_size = format_str_to_bytes(max_size)

        total_size, result_keys = 0, []
        meta_dict = self._get_all_cache_meta()

        for cache_key in sorted(meta_dict, key=self._clean_sorting_func, reverse=True):
            total_size += meta_dict[cache_key].object_size
            if total_size > max_size:
                result_keys.append(cache_key)

        return result_keys

    @property
    def _clean_sorting_func(self) -> Callable:
        """Get function that will be used for cache keys sorting.

        Result function depends on ``autoclean_mode`` parameter:
            - if it's "last_used", then result function will return file access time
            - if it's "last_created", then result function will return file creation time
        """
        if self.autoclean_mode == 'last_used':
            return self._get_access_time_by_cache_key
        elif self.autoclean_mode == 'last_created':
            return self._get_creation_time_by_cache_key
        else:
            raise ValueError(f'Unknown ``autoclean_mode`` value: {self.autoclean_mode}')

    def _get_access_time_by_cache_key(self, cache_key: CacheKey) -> float:
        """Get file access time using cache key."""
        pickle_path = self._handler.get_cache_pickle_path(cache_key)
        return get_file_access_time(filename=str(pickle_path))

    def _get_creation_time_by_cache_key(self, cache_key: CacheKey) -> float:
        """Get file creation time using cache key."""
        return self.__meta_cache__[cache_key].creation_timestamp  # type: ignore


def cache_autoclean(func: F) -> F:
    """Decorator to automatically call ``self.clean`` after each function call.

    Decorator can be applied only to ``CacheController`` class methods.
    """
    if not func.__qualname__.startswith('CacheController.'):
        raise ValueError(
            'Decorator ``cache_autoclean`` can only be applied to ``CacheController`` methods',
        )

    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        result = func(self, *args, **kwargs)
        if self.autoclean:
            self.clean()
        return result
    return cast(F, wrapper)
