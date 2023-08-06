import contextlib
from functools import wraps
from typing import (
    Any,
    Callable,
)


def sklearn_required(func: Callable) -> Callable:
    """Decorator notifies that scikit-learn is required for decorated func."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except ImportError:
            from .. import __package_name__
            raise ImportError(
                f'Package "{__package_name__}" requires installed "scikit-learn" package '
                'to work with estimators',
            )
    return wrapper


def is_estimator(obj: Any) -> bool:
    """Check if object is an ``sklearn.BaseEstimator`` instance.

    NOTE: This check works without installed sklearn package.
    """
    with contextlib.suppress(Exception):
        if (
            'BaseEstimator' in str(obj.__class__.__mro__)
            and hasattr(obj, 'fit')
            and type(obj) is not type  # not class! must be instance
        ):
            return True

    return False


@sklearn_required
def get_estimator_params(estimator: Any, all_params: bool = False) -> dict:
    """Get dict with estimator params."""
    from sklearn.utils._pprint import _changed_params
    return estimator.get_params() if all_params else _changed_params(estimator)  # type: ignore


@sklearn_required
def is_fitted_estimator(estimator: Any) -> bool:
    """Check if estimator is fitted or not."""
    from sklearn.exceptions import NotFittedError
    from sklearn.utils.validation import check_is_fitted

    try:
        check_is_fitted(estimator)
        return True
    except NotFittedError:
        return False
