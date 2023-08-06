from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression

from scikit_cache.controller import CacheController
from scikit_cache.utils.estimators import is_fitted_estimator
from tests.conftest import TEST_CACHE_DIR

cache = CacheController(cache_dir=TEST_CACHE_DIR, logger='logger', autoclean=False)


def test_make_cached_estimator():
    """Test that ``make_cached_estimator`` adds extra attrs to class and instance."""
    estimator = LinearRegression()
    assert not hasattr(LinearRegression, '__cache_ctrl__')
    assert not hasattr(LinearRegression, '__original_fit__')

    with cache.make_cached_estimator(estimator) as cached_estimator:
        # Cache controller is added to both class and instance
        assert LinearRegression.__cache_ctrl__ is cache
        assert cached_estimator.__cache_ctrl__ is cache

        # Objects are the same instance
        assert cached_estimator is estimator

        # Extra method added too
        assert hasattr(LinearRegression, '__original_fit__')
        assert hasattr(estimator, '__original_fit__')

    # After context manager - class no longer has controller
    assert not hasattr(LinearRegression, '__cache_ctrl__')
    assert not hasattr(LinearRegression, '__original_fit__')
    assert not hasattr(estimator, '__cache_ctrl__')
    assert not hasattr(estimator, '__original_fit__')


def test_fit_cached_estimator(mocker):
    """Test fitting estimator wrapped by ``make_cached_estimator``."""
    cache.wipe()

    estimator = LinearRegression()
    assert not is_fitted_estimator(estimator)

    iris = load_iris(as_frame=True)

    from scikit_cache.components.estimators import estimator_logger

    # Mock logs
    mocked_info = mocker.patch.object(estimator_logger, 'info')
    mocked_warning = mocker.patch.object(estimator_logger, 'warning')

    with cache.make_cached_estimator(estimator) as cached_estimator:
        # 1. Cache disabled - fit() calls original method
        cached_estimator.fit(X=iris.data, y=iris.target)
        assert is_fitted_estimator(cached_estimator)

        # No cache logs
        mocked_info.assert_not_called()
        mocked_warning.assert_not_called()

        # 2. Cache enabled - going to cache for fit results
        cache.enable(cache_estimators=True)
        cached_estimator.fit(X=iris.data, y=iris.target)

        # Cache miss
        mocked_warning.assert_called_once()
        assert mocked_warning.call_args[0][0] == 'estimator cache miss'
        mocked_warning.reset_mock()

        # Writing new cache
        mocked_info.assert_called_once()
        assert mocked_info.call_args[0][0].startswith('estimator cache write')
        mocked_info.reset_mock()

        # 3. Cache enabled and saved before
        cached_estimator.fit(X=iris.data, y=iris.target)

        # Cache hit
        mocked_info.assert_called_once()
        assert mocked_info.call_args[0][0].startswith('estimator cache hit')
        mocked_info.reset_mock()

        # Just no warnings
        mocked_warning.assert_not_called()

    cache.disable()
    cache.wipe()
