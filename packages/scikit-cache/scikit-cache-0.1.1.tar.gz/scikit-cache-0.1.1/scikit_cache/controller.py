import logging
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    PrivateAttr,
    validator,
)

from scikit_cache.utils import (
    format_bytes_to_str,
    format_str_to_bytes,
    get_func_name,
    get_installed_packages,
    get_pickle_version,
    get_python_version,
    get_self_version,
    get_username,
)

from .components import (
    CleanUpMixin,
    DecoratorMixin,
    EstimatorsMixin,
    FileCacheHandler,
    InternalCacheMixin,
    LoggingMixin,
    cache_autoclean,
)
from .resources import (
    BaseCacheMeta,
    CacheKey,
    ObjCacheMeta,
)

controller_logger = logging.getLogger('scikit_cache.controller')


class CacheController(
    InternalCacheMixin,
    LoggingMixin,
    CleanUpMixin,
    DecoratorMixin,
    EstimatorsMixin,
    BaseModel,
):
    """Cache controller class.

    Main class for cache control. Allows to make decorated functions using ``cache.decorator``
    method or set/get objects to cache using ``cache.get()`` and ``cache.set()`` methods.

    NOTE: Some of class methods are stored in mixin classes like ``DecoratorMixin`` or
    ``CleanUpMixin``. This was made to split up some of logic to several files.

    :param cache_dir: directory to store pickled cache objects. Default is ".scikit_cache" in
        current directory.
    :param author: Author name to store in cache meta. Can be used for team cache folder. Default
        is current username.
    :param logger: logging mode. Can be following types:
        - "print" string to use built-in print function to display logs
        - "logger" string to use python built-in "logging.Logger" (by default)
        - None to disable logging
    :param autoclean: enable cache autoclean by TTL on each cache call or not. Allows to
        automatically call ``cache.clean`` on each cache set/get operation. Slows down cache
        operations a bit. Default is True.
    :param autoclean_mode: mode for autoclean if ``max_cached_objects`` or ``max_cache_dir_size``
        options are enabled. Two modes exist:
        - "last_used": if cache exceeded then delete oldest cache objects by their usage time.
            Set as default mode.
        - "last_created": if cache exceeded then delete oldest cache objects by their creation time.
    :param max_cached_objects: The maximum number of items the cache will store before it starts
        deleting some. Default value is ``None`` = unlimited number of items.
    :param max_cache_dir_size: The maximum size of cache directory. Can be string like "10GB",
        "128MB" or integer number that equals size in bytes. Default is None = no limitations.
    :param default_ttl: default TTL for all cached objects (in seconds). All objects older that TTL
        will be automatically deleted on next cache call if ``autoclean=True``. Default value is
        "-1" that means infinite TTL. Custom TTL can be specified in ``cache.set()`` or
        ``cache.decorator()`` for single cached object.
    :param cache_handler_class: name for cache handler. Currently only "FileCacheHandler" is
        available (by default).
    :param check_python_version: enable python version check on cache get or not. Default is True.
    :param check_pickle_version: enable ``pickle`` package version check on cache get or not.
        Default is True.
    :param check_self_version: enable self package version check on cache get or not.
        Default is True.
    :param check_func_source: The default condition applied to decorator ``cache.decorator`` only
        which controls if the source code of the function should be included when forming the hash
        which is used as the cache key. This ensures that if the source code changes, the cached
        value will not be returned when the new function is called even if the arguments are th
        same. Defaults to True.
    :param check_version_level: level of version depth comparison for ``check_python_version``,
        ``check_pickle_version``, ``check_self_version`` and ``check_packages`` parameters.
        Default is level 2.
        For example:
            - Level 1: Compare only major version. "3.6" and "3.7" will be equal if level = 1.
            - Level 2: Compare major and minor versions. "3.6" and "3.7" will be treated as
                different, but "3.6.3" and "3.6.12" will be equal.
            - Level 3: Full comparison (major, minor, fix versions).
    """

    # Base parameters
    cache_dir: str = './.scikit_cache'
    author: str = Field(default_factory=get_username)
    logger: Optional[str] = 'logger'

    # Cache autoclean parameters
    autoclean: bool = True
    autoclean_mode: Literal['last_used', 'last_created'] = 'last_used'
    max_cached_objects: Optional[int] = None
    max_cache_dir_size: Optional[Union[int, str]] = None  # in bytes or can be string like "10GB"
    default_ttl: int = -1  # in seconds, -1 means infinite ttl

    # Cache handler
    cache_handler_class: str = 'FileCacheHandler'

    # Version check params
    check_python_version: bool = True
    check_pickle_version: bool = True
    check_self_version: bool = True
    check_func_source: bool = True  # check if hash of function changed or not
    check_external_packages: Union[bool, List[str]] = False
    check_version_level: int = 2  # e.g 3.7.1 and 3.7.2 -> both has 3.7 (level=2)

    # Current versions/packages for meta (NOTE: no need to override them)
    python_version: str = Field(default_factory=get_python_version)
    pickle_version: str = Field(default_factory=get_pickle_version)
    self_version: str = Field(default_factory=get_self_version)
    installed_packages: Dict[str, str] = Field(default_factory=get_installed_packages)

    # Internal attributes
    __enabled_for_estimators__: bool = PrivateAttr(default=False)
    __enabled_for_functions__: bool = PrivateAttr(default=False)
    __mode__: str = PrivateAttr(default='rw')
    __only_functions__: List[str] = PrivateAttr(default_factory=list)
    __excluded_functions__: List[str] = PrivateAttr(default_factory=list)
    __meta_cache__: Dict[str, Optional[ObjCacheMeta]] = PrivateAttr(default_factory=dict)
    __child_keys_cache__: Dict[str, List[CacheKey]] = PrivateAttr(default_factory=dict)

    class Config:
        arbitrary_types_allowed = True

    # Public methods
    # =============================================================================================

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> CacheKey:
        """Set object to cache by key.

        :param key: string cache key (not ``CacheKey`` instance)
        :param value: any object to store in cache
        :param ttl: optional TTL for specific cached object (in seconds). Set to -1 for
            infinite TTL. Set to None to use ``cache.default_ttl`` value (by default).
        :return: generated ``CacheKey`` instance
        """
        key_ttl = ttl if ttl is not None else self.default_ttl
        cache_key = CacheKey.from_raw_key(raw_key=key)
        cache_meta = ObjCacheMeta.from_raw_key(key, key_ttl, self._base_meta)
        self._set(key=cache_key, value=value, meta=cache_meta)
        return cache_key

    def get(self, key: str) -> Tuple[bool, Any]:
        """Get object from cache.

        :param key: string cache key (not ``CacheKey`` instance)
        :return: tuple with hit or not (boolean), and cached value (if cache hit)
        """
        cache_key = CacheKey.from_raw_key(raw_key=key)
        return self._get(key=cache_key)

    def delete(self, *keys: str) -> int:
        """Delete object(s) from cache.

        :param keys: one or multiple string cache keys (not ``CacheKey`` instances)
        :return: number of deleted objects
        """
        return self._delete(*(CacheKey.from_raw_key(raw_key=key) for key in keys))

    def enable(
        self,
        cache_functions: bool = True,
        cache_estimators: bool = True,
        only_functions: Optional[List[Callable]] = None,
        exclude_functions: Optional[List[Callable]] = None,
        mode: Literal['r', 'w', 'rw'] = 'rw',
    ) -> None:
        """Enable cache.

        Cache enabling affects following objects:
            - functions that were decorated by ``cache.decorator``
            - estimators that were wrapped using ``cache.make_cached_estimator``

        By default, all cache is disabled until ``cache.enable()`` function is called. To disable
        cache use ``cache.disable()`` function.

        :param cache_functions: if True, then cache will be enabled for decorated functions.
            Default is True. More info in ``cache.decorator`` function.
        :param cache_estimators: if True, then cache will be enabled for estimators.
            Default is True. More info in ``cache.make_cached_estimator`` function.
        :param only_functions: list of functions to enable cache. Works as whitelist. All functions
            that not specified in this list will not use cache. By default, ``only_functions`` is
            None that means all functions will use cache.
        :param exclude_functions: list of functions to not enable cache. Works as blacklist. All
            decorated functions will use cache except this list. By default, ``exclude_functions``
            is None that means all functions will use cache.
        :param mode: mode of cache work.
            - "rw": read-write mode. Set by default. Allows to both read cached values (on cache
                hit) and write new cached values (on cache miss).
            - "r": read-only mode. Only read already cached values, no writing new values.
            - "w": write-only mode. Only write cached values to file, not reading cache. We don't
                recommend to use this mode, as it will generate new cache objects on each call
                even if function args/kwargs are the same.
        :return: None
        """
        if only_functions and exclude_functions:
            raise ValueError('Specify ``only_functions`` or ``exclude_functions``, not both')

        available_modes = {'r', 'w', 'rw'}
        if mode not in available_modes:
            raise ValueError(f'Unknown mode: {mode}. Available modes: {available_modes}')

        if only_functions:
            self.__only_functions__ = [get_func_name(func) for func in only_functions]

        if exclude_functions:
            self.__excluded_functions__ = [get_func_name(func) for func in exclude_functions]

        self.__enabled_for_functions__ = cache_functions
        self.__enabled_for_estimators__ = cache_estimators
        self.__mode__ = mode
        self._log(f'cache enabled :: {self.cache_dir}', logger=controller_logger)

    def disable(self) -> None:
        """Disable cache.

        Cache disabling affects decorated functions and cached estimators. By default, all cache is
        disabled until ``cache.enable()`` function is called. To disable cache use
        ``cache.disable()`` function.

        It doesn't remove files from cache dir. Use ``cache.clean()`` or ``cache.wipe()`` methods
        to clean cache.
        """
        if not self.__enabled_for_functions__ and not self.__enabled_for_estimators__:
            self._log('cache already disabled', level='warning', logger=controller_logger)
            return None

        self.__enabled_for_functions__ = False
        self.__enabled_for_estimators__ = False
        self._log('cache disabled', logger=controller_logger)

    @property
    def is_enabled_for_estimators(self) -> bool:
        """Check if cache is enabled for estimators or not.

        See ``EstimatorsMixin`` for more info.
        """
        return self.__enabled_for_estimators__

    @property
    def is_enabled_for_functions(self) -> bool:
        """Check if cache is enabled for all decorated functions or not.

        See ``DecoratorMixin`` for more info.
        """
        return self.__enabled_for_functions__

    @property
    def is_enabled_for_any(self) -> bool:
        """Check if cache enabled by any point."""
        return self.is_enabled_for_estimators or self.is_enabled_for_functions

    @property
    def mode(self) -> str:
        """Get current cache mode.

        Mode can be:
            - "r" - read cache only and not writing new cache
            - "w" - write to cache only without reading (this is not useful mode at all)
            - "rw" (default) - read and write to cache
        """
        return self.__mode__

    def is_enabled_for_func(self, func: Callable) -> bool:
        """Check if caching should be used on specific decorated function.

        Method checks if function name is in whitelist (``self.__only_functions__``) or blacklist
        (``self.__excluded_functions__``) of cache functions.

        :param func: callable function
        :return: True if cache is enabled for func else False
        """
        if not self.is_enabled_for_functions:
            return False

        func_name = get_func_name(func)

        if self.__only_functions__:
            return func_name in self.__only_functions__

        if self.__excluded_functions__:
            return func_name not in self.__excluded_functions__

        return True

    def clean(
        self,
        clean_objects_by_ttl: bool = True,
        max_cached_objects: Optional[int] = None,
        max_cache_dir_size: Optional[Union[str, int]] = None,
    ) -> int:
        """Clean old cached objects depending on TTL, max objects or max size.

        Method performs cleaning of cache dir due to multiple rules:
            - All cached objects with expired TTL will be deleted
            - Remove cached objects if ``max_cached_objects`` option enabled
            - Remove cached objects if ``max_cache_dir_size`` option enabled

        This method is automatically called on each cache get/set in ``autoclean`` option is enabled
        by user. Also you can manually call ``cache.clean(...)`` with different params.

        :param clean_objects_by_ttl: enabled deleting objects with expired TTL or not.
        :param max_cached_objects: max objects in cache dir. Default value is stored in cache
            controller.
        :param max_cache_dir_size: max size of cache dir. Default value is stored in cache
            controller.
        :return: number of deleted objects
        """
        to_remove: Set[CacheKey] = set()
        removed_keys: int = 0

        if clean_objects_by_ttl:
            to_remove.update(self._get_clean_objects_by_expired_tl())

        max_cached_objects = max_cached_objects or self.max_cached_objects
        if max_cached_objects is not None:
            to_remove.update(self._get_clean_objects_by_max_number(max_cached_objects))

        max_cache_dir_size = max_cache_dir_size or self.max_cache_dir_size
        if max_cache_dir_size is not None:
            to_remove.update(self._get_clean_objects_by_max_size(max_cache_dir_size))

        if to_remove:
            self._delete(*to_remove)

            removed_keys = len(to_remove)
            self._log(f'cleaned cache keys: {removed_keys}', logger=controller_logger)

        return removed_keys

    def keys(self) -> List[CacheKey]:
        """Get list of existing cache keys."""
        return list(self._get_all_cache_meta())

    def wipe(self) -> None:
        """Wipe cache directory.

        NOTE: Removes cache directory itself. Don't store any other files in cache directory!
        """
        self._handler.wipe_cache_dir()
        self._invalidate_internal_cache(clear_all=True)
        self._log('cache wiped', logger=controller_logger)

    def info(
        self,
        display: Union[bool, Callable] = True,
        keys: bool = False,
        full: bool = False,
        show_total: bool = True,
        show_packages: bool = True,
    ) -> Optional[dict]:
        """Get info about cache.

        :param display: if True, then print cache info to stdout. If False, then return dict
            with cache info. Also can accept any callable to use different function for displaying
            output (for example: ``display=logging.info``).
        :param keys: show all cache keys or not. Default is False
        :param full: show full cache statistics or not. Default is False.
        :param show_total: show total cache statistsics or not
        :param show_packages: show packages if full=True
        :return: optional dict with cache meta if display = False
        """
        from . import __package_name__

        self._init_internal_cache(invalidate_first=True)

        meta_dict = self._get_all_cache_meta()
        if not display:
            return meta_dict

        _: Callable = print if display is True else display  # type: ignore # noqa

        total_size = 0
        for key, meta in meta_dict.items():
            total_size += meta.object_size or 0
            if not keys:
                continue

            cache_path = ' / '.join(key.split('__'))
            _(f'\n{cache_path}\n{"-" * len(cache_path)}')
            _(f'Date: {meta.creation_time_formatted}')
            _(f'Size: {meta.object_size_formatted}')

            if full:
                _(f'Author: {meta.author}')
                _(
                    f'Versions: python {meta.python_version}, pickle {meta.pickle_version}, '
                    f'{__package_name__}: {meta.self_version}',
                )
                if meta.raw_key:
                    _(f'Original key: {meta.raw_key}')
                if meta.func_name:
                    _(f'Func name: {meta.func_name}')
                if meta.func_code_hash:
                    _(f'Func hash: {meta.func_code_hash}')
                if meta.func_args_kwargs:
                    _(f'Func args: {meta.func_args_kwargs["args"]}')
                    _(f'Func kwargs: {meta.func_args_kwargs["kwargs"]}')

                if show_packages:
                    _(f'Packages: {", ".join(repr(p) for p in (meta.installed_packages or []))}')

        if show_total:
            _('\nCACHE STATISTICS\n================')
            _(f'Keys: {len(meta_dict)}')
            _(f'Size: {format_bytes_to_str(total_size)}')

        return None

    # Private methods
    # =============================================================================================

    def __setattr__(self, name: str, value: Any) -> None:
        if name == 'cache_dir' and self.cache_dir != value:
            controller_logger.info(
                f'Cache directory changed from "{self.cache_dir}" to "{value}"',
            )
            self._invalidate_internal_cache(clear_all=True)

        super().__setattr__(name, value)

    def __repr__(self) -> str:
        """Object repr."""
        return f'<CacheController: {self.cache_dir}>'

    def _init_private_attributes(self) -> None:
        """Pydantic method `_init_private_attributes`.

        We use this method as alternative to `__post_init__` to do anything after object init.
        """
        super()._init_private_attributes()
        self._init_internal_cache()

    @cache_autoclean
    def _set(self, key: CacheKey, value: Any, meta: ObjCacheMeta) -> None:
        """Low-level function to set cache by key and write meta.

        :param key: ``CacheKey`` instance
        :param value: object that will be stored in cache
        :param meta: cache meta information (author, datetime and etc.)
        :return:
        """
        self._invalidate_internal_cache(key)
        self.__meta_cache__[key] = meta
        return self._handler.set(key, value, meta)

    @cache_autoclean
    def _get(self, key: CacheKey) -> Tuple[bool, Any]:
        """Low-level function to get cache by key.

        Method required generated cache key.

        :param key: ``CacheKey`` instance
        :return: tuple with hit or not (boolean), and cached value (if cache hit)
        """
        return self._handler.get(key)

    def _delete(self, *keys: CacheKey) -> int:
        """Low-level function to delete cache by keys.

        :param keys: ``CacheKey`` instances
        :return: number of deleted objects
        """
        deleted_keys = sum(self._handler.delete(key) for key in keys)
        self._invalidate_internal_cache(*keys)
        return deleted_keys

    @property
    def _handler(self) -> FileCacheHandler:
        """Get cache handler instance."""
        return FileCacheHandler(cache_dir=self.cache_dir)

    @property
    def _base_meta(self) -> 'BaseCacheMeta':
        """Initialize cache meta information instance."""
        return BaseCacheMeta(
            author=self.author,
            python_version=self.python_version,
            pickle_version=self.pickle_version,
            self_version=self.self_version,
            installed_packages=self.installed_packages,
        )

    def _collect_external_packages(self, only_packages: Optional[List[str]] = None) -> List[str]:
        if self.check_external_packages is False:
            return []

        installed_packages: List[str] = (
            self.check_external_packages
            if isinstance(self.check_external_packages, list)
            else list(self.installed_packages)
        )
        if not only_packages:
            return sorted(installed_packages)

        return sorted(set(installed_packages) & set(only_packages))

    # Data validation
    # =============================================================================================

    @validator('max_cache_dir_size')
    def _max_cache_dir_size_validator(cls, value: Union[int, str]) -> int:
        """Validate `max_cache_dir_size` field."""
        if isinstance(value, str):
            value = format_str_to_bytes(value)
        return value
