from typing import (
    Dict,
    List,
    Optional,
    Set,
)

from ..resources import (
    CacheKey,
    ObjCacheMeta,
)


class InternalCacheMixin:
    """Mixin for ``CacheController`` class with internal (private) methods only."""

    def _get_cache_meta(self, key: CacheKey) -> Optional[ObjCacheMeta]:
        """Get cache meta by key.

        Proxied method from cache_handler with internal caching.
        """
        if key in self.__meta_cache__:
            return self.__meta_cache__[key]  # type: ignore

        meta: Optional[ObjCacheMeta] = self._handler.get_cache_meta(key)
        self.__meta_cache__[key] = meta  # save to internal cache
        return meta

    def _get_all_cache_meta(self) -> Dict[CacheKey, ObjCacheMeta]:
        """Get all cache meta."""
        return {k: v for k, v in self.__meta_cache__.items() if v is not None}

    def _find_child_keys(self, key: CacheKey) -> List[CacheKey]:
        """Get child keys for current key.

        Proxied method from cache_handler with internal caching.
        """
        if key in self.__child_keys_cache__:
            return self.__child_keys_cache__[key]  # type: ignore

        child_keys: List[CacheKey] = self._handler.find_child_keys(key)
        self.__child_keys_cache__[key] = child_keys  # save to internal cache
        return child_keys

    def _init_internal_cache(self, invalidate_first: bool = False) -> None:
        """Warm internal cache.

        Method searches for all existing cache keys and meta files and add them to internal cache.
        """
        if invalidate_first:
            self._invalidate_internal_cache(clear_all=True)

        root_key = CacheKey('__root__')

        for child_key in self._handler.find_child_keys(root_key):
            parent_key = []
            for part in child_key.split('__'):
                parent_key.append(part)
                self._find_child_keys(key=CacheKey('__'.join(parent_key)))
            self._get_cache_meta(child_key)  # warm meta cache

    def _invalidate_internal_cache(self, *keys: CacheKey, clear_all: bool = False) -> int:
        """Invalidate internal controller cache.

        Method can invalidate only specific cache keys or drop all internal cache if parameter
        ``clear_all`` is True.
        """
        if clear_all:
            dropped_amount = len(self.__meta_cache__)
            self.__meta_cache__.clear()
            self.__child_keys_cache__.clear()
            return dropped_amount

        keys_to_drop: Set[CacheKey] = set()
        for key in keys:
            if not isinstance(key, CacheKey):
                raise TypeError(f'Key must be ``CacheKey`` instance, not {type(key)}')

            keys_to_drop.update(key.get_parent_keys())

        for key in keys_to_drop:
            self.__meta_cache__.pop(key, None)
            self.__child_keys_cache__.pop(key, None)

        return len(keys_to_drop)
