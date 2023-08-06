from datetime import datetime
from functools import cached_property
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)

from pydantic import (
    BaseModel,
    Field,
    validator,
)

from scikit_cache.utils import (
    compare_versions,
    format_bytes_to_str,
    get_datetime_str,
    get_func_name,
    get_random_hex,
    hash_for_callable,
    hash_for_iterable,
    hash_for_simple_object,
    yaml_repr,
)


class CacheKey(str):
    """Structure to store cache key.

    Purpose of this objects is to explicitly match cached value using unique identificator.
    """

    def __repr__(self) -> str:
        """Object repr."""
        return f'<CacheKey: {self}>'

    @classmethod
    def from_raw_key(cls, raw_key: str, prefix: str = 'raw') -> 'CacheKey':
        """Create cache key from raw string key."""
        if type(raw_key) is not str:  # `isinstance` works incorrectly here with ``CacheKey``
            raise TypeError(f'Key must be string, not {type(raw_key)}')

        nested_key = '__'.join(filter(bool, [  # type: ignore
            prefix,
            hash_for_simple_object(raw_key),
        ]))
        return cls(nested_key)

    @classmethod
    def from_func(
        cls,
        func: Callable,
        func_args: Optional[tuple] = None,
        func_kwargs: Optional[dict] = None,
    ) -> 'CacheKey':
        """Generate cache key from function.

        Generates nested key for passed func and arguments.

        :param func: function (callable) that returned result
        :param func_args: function arguments
        :param func_kwargs: function keyword arguments
        :return: cache key instance
        """
        nested_key = '__'.join(filter(bool, [  # type: ignore
            get_func_name(func),
            hash_for_iterable([func_args or None, func_kwargs or None]),
        ]))
        return cls(nested_key)

    def add_random_part(self) -> 'CacheKey':
        """Generate new cache key with extra random part."""
        return self.__class__(f'{self}__{get_random_hex()}')

    @classmethod
    def from_filepath(cls, path: Union[str, Path]) -> 'CacheKey':
        """Generate cache key from file path.

        For example:
            >>> CacheKey.from_filepath(path='root/home/key')
            "root__home__key""

        :param path: file path
        :return: cache key instance
        """
        nested_key = '__'.join(str(path).split('/'))
        return cls(nested_key)

    @cached_property
    def as_filepath(self) -> str:
        """Represent cache key as filesystem path."""
        if not self:
            raise ValueError('CacheKey has empty nested key')

        if self == '__root__':
            return ''

        return '/'.join(self.split('__'))

    def get_parent_keys(self, include_self: bool = True) -> List['CacheKey']:
        """Get keys for parent.

        For example:
            >>> key = CacheKey('foo__bar__buzz')
            >>> key.get_parent_keys(include_self=True)
            [CacheKey("foo"), CacheKey("foo__bar"), CacheKey("foo__bar__buzz")]
            >>> key.get_parent_keys(include_self=False)
            [CacheKey("foo"), CacheKey("foo__bar")]
        """
        return [
            CacheKey(self.rsplit('__', size)[0])
            for size in range(self.count('__'), -1 if include_self else 0, -1)
        ]


class BaseCacheMeta(BaseModel):
    """Base cache meta.

    Base meta contains global information about who and when added specific key to cache.
    """

    author: str
    python_version: str
    pickle_version: str
    self_version: str
    installed_packages: Dict[str, str]


class ObjCacheMeta(BaseCacheMeta):
    """Object cache beta."""

    creation_time: str = Field(default_factory=get_datetime_str)
    ttl: int
    object_size: int = 0  # updated after saving file on disk

    func_name: Optional[str] = None  # only for decorated functions
    func_code_hash: Optional[str] = None  # only for decorated functions
    func_args_kwargs: Optional[Dict[str, Any]] = None  # only for decorated functions
    raw_key: Optional[str] = None  # only for raw values

    def __str__(self) -> str:
        return f'<{self.__class__.__name__}: {self.creation_time}>'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.creation_time}>'

    @property
    def creation_time_formatted(self) -> str:
        """Get datetime as formatted string."""
        return self.creation_datetime_obj.strftime('%Y-%m-%d %H:%M')

    @property
    def creation_timestamp(self) -> float:
        return self.creation_datetime_obj.timestamp()

    @property
    def creation_datetime_obj(self) -> datetime:
        return datetime.fromisoformat(self.creation_time)

    @property
    def object_size_formatted(self) -> str:
        """Get formatted object size."""
        return format_bytes_to_str(self.object_size) if self.object_size else '-'

    @classmethod
    def from_raw_key(
        cls,
        raw_key: str,
        ttl: int,
        base_meta: BaseCacheMeta,
    ) -> 'ObjCacheMeta':
        if type(raw_key) is not str:  # `isinstance` works incorrectly here with ``CacheKey``
            raise TypeError(f'Key must be string, not {type(raw_key)}')

        return cls(raw_key=raw_key, ttl=ttl, **base_meta.dict())

    @classmethod
    def from_func(
        cls,
        func: Callable,
        func_args: Optional[tuple],
        func_kwargs: Optional[dict],
        fixed_hash: Optional[str],
        func_ttl: int,
        base_meta: BaseCacheMeta,
    ) -> 'ObjCacheMeta':
        """Generate cache meta from function.

        :param func: function (callable) that returned result
        :param func_args: function arguments
        :param func_kwargs: function keyword arguments
        :param func_ttl: function TTL in seconds
        :param fixed_hash: fixed func code hash (for example, from decorator params)
        :param base_meta: instance of ``BaseCacheMeta``
        :return: cache meta instance
        """
        return cls(
            func_name=get_func_name(func),
            func_code_hash=fixed_hash or hash_for_callable(func, include_name=False),
            func_args_kwargs={
                'args': yaml_repr(func_args or []),
                'kwargs': yaml_repr(func_kwargs or {}),
            },
            ttl=func_ttl,
            **base_meta.dict(),
        )

    def is_similar_to(
        self,
        to: 'ObjCacheMeta',
        check_python_version: bool = True,
        check_pickle_version: bool = True,
        check_self_version: bool = True,
        check_func_source: bool = True,
        check_external_packages: Union[bool, List[str]] = False,
        check_version_level: int = 2,
    ) -> bool:
        """Compare two ``ObjCacheMeta`` objects using specific checks."""
        # 1. Check python versions
        if (
            check_python_version
            and not compare_versions(self.python_version, to.python_version, check_version_level)
        ):
            return False

        # 2. Check pickle versions
        if (
            check_pickle_version
            and not compare_versions(self.pickle_version, to.pickle_version, check_version_level)
        ):
            return False

        # 3. Check self version
        if (
            check_self_version
            and not compare_versions(self.self_version, to.self_version, check_version_level)
        ):
            return False

        # 4. Check packages versions
        if check_external_packages:
            # compare packages versions that exist in both ``ObjCacheMeta`` objects
            packages_to_compare = set(self.installed_packages) & set(to.installed_packages)

            # if check_packages is a list -> compare only specific packages
            if isinstance(check_external_packages, list):
                packages_to_compare &= set(check_external_packages)

            for package_name in packages_to_compare:
                if not compare_versions(
                    version_a=self.installed_packages[package_name],
                    version_b=to.installed_packages[package_name],
                    level=check_version_level,
                ):
                    return False

        # 5. Check func hash
        if check_func_source and self.func_code_hash != to.func_code_hash:
            return False

        return True

    @validator('raw_key')
    def raw_key_length_validator(cls, value: Optional[str]) -> Optional[str]:
        """Validate `max_cache_dir_size` field."""
        if not value:
            return value

        val_len = len(value)
        return value if val_len <= 50 else f'{value[:50]} (len = {val_len})'
