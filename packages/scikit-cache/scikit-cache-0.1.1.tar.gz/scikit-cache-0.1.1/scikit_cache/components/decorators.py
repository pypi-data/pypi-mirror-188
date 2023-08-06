import logging
from functools import wraps
from typing import (
    Any,
    Callable,
    List,
    Optional,
    Tuple,
)

from ..resources import (
    CacheKey,
    ObjCacheMeta,
)
from ..utils import (
    CACHE_HIT_ATTR,
    format_bytes_to_str,
)

decorator_logger = logging.getLogger('scikit_cache.decorator')


class DecoratorMixin:
    """Mixin for ``CacheController`` class with cache decorator."""

    def decorator(
        self,
        ignored_kwargs: Optional[List[str]] = None,
        external_packages: Optional[List[str]] = None,
        ttl: Optional[int] = None,
        fixed_hash: Optional[str] = None,
    ) -> Callable:
        """Decorator for function caching.

        Cache key will be automatically generated using:
            - full function name (module path + name)
            - passed args/kwargs
            - current state of function code

        By default, if cache is not enabled yet, decorated function will works as normal, without
        cache. When cache is activated (using ``cache.enable()`` function) then decorated function
        will check existing cache and save new cache too.

        Additionally, decorated function can accepts extra ``use_cache`` keyword argument to
        manually enable/disable caching on function call. For example: ``foo(..., use_cache=True)``
        will enable cache just for this call of ``foo`` function using default parameters even if
        ``CacheController`` is not yet enabled.

        On the over hand, ``use_cache=False`` allows to manually disable cache for specific func
        call even if cache is enabled.

        :param ignored_kwargs: list of kwarg names that will be ignored during creating cache key.
            Use it for params that don't affect function usage (like ``logger`` param and so on).
        :param external_packages: list of external packages names. It's a good practise to define
            all external packages that were used inside specific function. It allows to check
            less packages if ``check_external_packages`` option is enabled in ``CacheController``.
        :param ttl: optional TTL for specific decorated function (in seconds). Set to -1 for
            infinite TTL. Set to None to use ``cache.default_ttl`` value (by default).
        :param fixed_hash: fixed func code hash. Use any string as hash to skip checking if
            function were modified or not. We do not recommend manually set func code hash as it may
            cause unexpected returning results of decorated function!
        :return: decorated function
        """
        def inner(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*func_args: Any, **func_kwargs: Any) -> Any:
                # Force cache enabled if function called like "my_func(..., use_cache=True)"
                force_use_cache = func_kwargs.pop('use_cache', None)

                if force_use_cache is True:
                    if self.is_enabled_for_functions:
                        self._log(
                            'use_cache=True ignored, cache already enabled',
                            func=func,
                            level='warning',
                            logger=decorator_logger,
                        )
                elif force_use_cache is False:
                    if self.is_enabled_for_functions:
                        self._log(
                            'use_cache=False enabled, cache is ignored',
                            func=func,
                            level='warning',
                            logger=decorator_logger,
                        )
                    # Disable cache by force -> return result immediatelly
                    return func(*func_args, **func_kwargs)

                # Use cache only if it's enabled and func not in blacklist.
                # Or if force_use_cache=True
                use_cache = (
                    self.is_enabled_for_func(func)
                    if force_use_cache is None
                    else force_use_cache
                )

                if not use_cache:
                    # If cache is disabled (of func ignored), return func result immediately
                    return func(*func_args, **func_kwargs)

                if not func_args and not func_kwargs:
                    raise ValueError(
                        'Could not cache function that has no args/kwargs!\n'
                        f'Remove cache.decorator() from function {func} or add args/kwargs.',
                    )

                # Build cache key and meta object for specific function call
                func_cache_key, func_meta = self._build_key_meta(
                    func=func,
                    func_args=func_args,
                    func_kwargs=func_kwargs,
                    ignored_kwargs=ignored_kwargs,
                    ttl=ttl,
                    fixed_hash=fixed_hash,
                )

                # Save to function new attribute to detect if result was retrieved from cache or not
                setattr(func, CACHE_HIT_ATTR, None)

                if 'r' in self.__mode__:
                    found, cached_result = self._func_cache_get(
                        func_cache_key=func_cache_key,
                        func_meta=func_meta,
                        external_packages=external_packages,
                    )
                    if found:
                        self._log(
                            'cache hit',
                            func=func,
                            level='info',
                            color='green',
                            logger=decorator_logger,
                        )
                        setattr(func, CACHE_HIT_ATTR, True)
                        return cached_result
                    else:
                        setattr(func, CACHE_HIT_ATTR, False)
                        self._log(
                            'cache miss',
                            func=func,
                            level='warning',
                            logger=decorator_logger,
                        )

                func_result = func(*func_args, **func_kwargs)

                if 'w' in self.__mode__:
                    self._func_cache_set(
                        func_cache_key=func_cache_key,
                        func_meta=func_meta,
                        func_result=func_result,
                    )
                    size = format_bytes_to_str(func_meta.object_size)
                    self._log(
                        f'cache write - {size}',
                        func=func,
                        level='info',
                        logger=decorator_logger,
                    )

                return func_result
            return wrapper
        return inner

    def _func_cache_set(
        self,
        func_cache_key: CacheKey,
        func_meta: ObjCacheMeta,
        func_result: Any,
    ) -> Tuple[CacheKey, ObjCacheMeta]:
        """High-level function to set cache for function result.

        :param func: function (callable) that returned result
        :param func_result: result that will be cached
        :param func_ttl: function TTL in seconds
        :param func_args: function arguments
        :param func_kwargs: function keyword arguments
        :param fixed_hash: fixed function code hash
        :return: generated cache key and cache meta (with object size)
        """
        cache_key = func_cache_key.add_random_part()
        self._set(key=cache_key, value=func_result, meta=func_meta)
        return cache_key, func_meta

    def _func_cache_get(
        self,
        func_cache_key: CacheKey,
        func_meta: ObjCacheMeta,
        external_packages: Optional[List[str]] = None,
    ) -> Tuple[bool, Any]:
        """High-level function to get cache result for function.

        :param func_cache_key: cache key of function
        :param func_meta: meta information about called function
        :param external_packages: list of specific packages to count when getting cached result.
        :return: tuple with hit or not (boolean), and cached value (if cache hit)
        """
        child_keys = self._find_child_keys(func_cache_key)
        for child_key in child_keys:
            child_meta: Optional[ObjCacheMeta] = self._get_cache_meta(child_key)
            if child_meta is None:
                continue

            if child_meta.is_similar_to(
                to=func_meta,
                check_python_version=self.check_python_version,
                check_pickle_version=self.check_pickle_version,
                check_self_version=self.check_self_version,
                check_func_source=self.check_func_source,
                check_external_packages=self._collect_external_packages(external_packages),
                check_version_level=self.check_version_level,
            ):
                return self._get(key=child_key)  # type: ignore

        return False, None

    def _filter_func_kwargs(
        self,
        func_kwargs: dict,
        ignored_kwargs: Optional[List[str]] = None,
    ) -> dict:
        """Get list of kwargs that will be used as cache key (and not ignored)."""
        return {
            k: func_kwargs[k] for k in func_kwargs if k not in ignored_kwargs
        } if ignored_kwargs else func_kwargs

    def _build_key_meta(
        self,
        func: Callable,
        func_args: tuple,
        func_kwargs: dict,
        ignored_kwargs: Optional[List[str]] = None,
        ttl: Optional[int] = None,
        fixed_hash: Optional[str] = None,
    ) -> Tuple[CacheKey, ObjCacheMeta]:
        """Build cache key and meta object for specific function call."""
        cachable_kwargs = self._filter_func_kwargs(func_kwargs, ignored_kwargs)
        func_cache_key = CacheKey.from_func(
            func=func,
            func_args=func_args,
            func_kwargs=cachable_kwargs,
        )
        func_meta = ObjCacheMeta.from_func(
            func=func,
            func_args=func_args,
            func_kwargs=cachable_kwargs,
            fixed_hash=fixed_hash,
            func_ttl=ttl if ttl is not None else self.default_ttl,
            base_meta=self._base_meta,
        )
        return func_cache_key, func_meta
