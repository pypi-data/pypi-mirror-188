import os
import pickle
import shutil
from pathlib import Path
from typing import (
    Any,
    List,
    Optional,
    Tuple,
)

import yaml  # type: ignore

from scikit_cache.utils import set_file_access_time

from ..resources import (
    CacheKey,
    ObjCacheMeta,
)

PICKLE_FILE = 'pickle.obj'
META_FILE = 'meta.yml'
ARGS_KWARGS_FILE = 'args_kwargs.yml'


class FileCacheHandler:
    """File cache handler.

    Sets/gets cached value to/from file directories.
    """

    def __init__(self, cache_dir: str):
        """Initialize class instance."""
        self.parent_cache_dir: Path = Path(cache_dir)

    def set(self, key: CacheKey, value: Any, meta: ObjCacheMeta) -> None:
        """Set value to file cache by key."""
        if not isinstance(key, CacheKey):
            raise TypeError(f'Key must be ``CacheKey`` instance, not {type(key)}')

        if not isinstance(meta, ObjCacheMeta):
            raise TypeError(f'Meta must be ``ObjCacheMeta`` instance, not {type(meta)}')

        cache_dir = self.parent_cache_dir / key.as_filepath
        cache_dir.mkdir(exist_ok=True, parents=True)

        pickle_file_path = cache_dir / PICKLE_FILE
        with open(pickle_file_path, 'wb') as f:
            pickle.dump(value, f)

        meta.object_size = pickle_file_path.stat().st_size
        with open(cache_dir / META_FILE, 'w') as f:
            yaml.dump(meta.dict(), f, allow_unicode=True)

        if meta.func_args_kwargs:
            args_kwargs = cache_dir.parent / ARGS_KWARGS_FILE
            if not args_kwargs.exists():
                with open(args_kwargs, 'w') as f:
                    yaml.dump(meta.func_args_kwargs, f, allow_unicode=True)

    def get(self, key: CacheKey) -> Tuple[bool, Any]:
        """Get value from cache by key."""
        if not isinstance(key, CacheKey):
            raise TypeError(f'Key must be ``CacheKey`` instance, not {type(key)}')

        try:
            # Manually set access time for cleanup mechanism
            pickle_path = self.get_cache_pickle_path(key)
            set_file_access_time(str(pickle_path), atime='now')

            with open(pickle_path, 'rb') as f:
                return True, pickle.load(f)
        except FileNotFoundError:
            return False, None

    def delete(self, key: CacheKey) -> bool:
        """Delete cache value."""
        if not isinstance(key, CacheKey):
            raise TypeError(f'Key must be ``CacheKey`` instance, not {type(key)}')

        cache_obj_dir = self.parent_cache_dir / key.as_filepath

        try:
            shutil.rmtree(cache_obj_dir)
            return True
        except FileNotFoundError:
            return False

    def get_cache_meta(self, key: CacheKey) -> Optional[ObjCacheMeta]:
        """Get cache meta by key."""
        meta_path = self.get_cache_meta_path(key)

        try:
            with open(meta_path, 'r') as f:
                return ObjCacheMeta(**yaml.safe_load(f))
        except FileNotFoundError:
            return None

    def get_cache_meta_path(self, key: CacheKey) -> Path:
        return self.parent_cache_dir / key.as_filepath / META_FILE

    def get_cache_pickle_path(self, key: CacheKey) -> Path:
        return self.parent_cache_dir / key.as_filepath / PICKLE_FILE

    def find_child_keys(self, key: CacheKey) -> List[CacheKey]:
        """Get child keys for current key."""
        child_keys = []
        cache_dir = self.parent_cache_dir / key.as_filepath

        for root, _, files in os.walk(cache_dir):
            if META_FILE in files and root != str(cache_dir):
                relative_path = Path(root).relative_to(self.parent_cache_dir)
                child_keys.append(CacheKey.from_filepath(relative_path))

        return child_keys

    def wipe_cache_dir(self) -> None:
        """Drop all existing cache.

        Removes cache directory completely.
        """
        shutil.rmtree(self.parent_cache_dir, ignore_errors=True)
