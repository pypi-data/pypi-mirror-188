import logging
from contextlib import contextmanager
from typing import Any

from ..resources import (
    CacheKey,
    ObjCacheMeta,
)
from ..utils import (
    format_bytes_to_str,
    hash_for_iterable,
)

estimator_logger = logging.getLogger('scikit_cache.estimator')


class EstimatorsMixin:
    """Mixin for cache controller to work with SKLearn estimators."""

    @contextmanager
    def make_cached_estimator(self, estimator: Any) -> Any:
        """Make estimator instance with cachable methods.

        This is context manager, works like this:

            with cache.make_cached_estimator(estimator) as cached_estimator:
                cached_estimator.fit()

        This function modifies existing estimator instance. Returned instance has same class but it
        containes modified ``.fit()`` method.

        This "cached estimator" can be used anywhere just as usual SKLearn estimator, but every
        time ``.fit()`` method is called it will go to cache to check if estimator was already
        calculated and cached.

        To enable caching for cached estimator - you need to enable cache using ``cache.enable()``
        function. By default, all cached estimator work as normal estimators.
        """
        estimator_class = estimator.__class__

        if not hasattr(estimator_class, '__original_fit__'):
            estimator_class.__original_fit__ = estimator_class.fit
            estimator_class.fit = self._estimator_fit_with_cache
            estimator_class.__cache_ctrl__ = self

        try:
            yield estimator
        finally:
            if hasattr(estimator_class, '__original_fit__'):
                estimator_class.fit = estimator_class.__original_fit__
                delattr(estimator_class, '__original_fit__')
                delattr(estimator_class, '__cache_ctrl__')

    @staticmethod
    def _estimator_fit_with_cache(instance: Any, *args: Any, **kwargs: Any) -> Any:
        """Function that implements ``BaseEstimator.fit()`` with cache mechanisms."""
        from sklearn.utils.validation import check_is_fitted

        cache = instance.__cache_ctrl__

        # If caching is disabled then use original ``.fit()`` function
        if not cache.is_enabled_for_estimators:
            return instance.__original_fit__(*args, **kwargs)

        # Get hash of all fit params including class and original parameters
        estimator_hash = hash_for_iterable((
            instance.__class__,
            instance.get_params(),
            args,
            kwargs,
        ))

        # Make cache key
        raw_key = f'estimators__{estimator_hash}'
        cache_key = CacheKey(raw_key)

        # Check if cached result exists (if read mode enabled)
        if 'r' in cache.__mode__:
            found, cached_result = cache._get(cache_key)
            if found:
                instance.__dict__ = cached_result.__dict__
                check_is_fitted(instance)
                cache._log(
                    'estimator cache hit',
                    level='info',
                    logger=estimator_logger,
                )
                return instance
            else:
                cache._log(
                    'estimator cache miss',
                    level='warning',
                    logger=estimator_logger,
                )

        # Call original ``.fit()`` function
        fit_result = instance.__original_fit__(*args, **kwargs)
        check_is_fitted(fit_result)

        # Save fit result to cache
        if 'w' in cache.__mode__:
            cache_meta = ObjCacheMeta(
                raw_key=raw_key,
                ttl=cache.default_ttl,
                **cache._base_meta.dict(),
            )
            cache._set(cache_key, fit_result, cache_meta)
            size = format_bytes_to_str(cache_meta.object_size)
            cache._log(
                f'estimator cache write - {size}',
                level='info',
                logger=estimator_logger,
            )

        return fit_result
