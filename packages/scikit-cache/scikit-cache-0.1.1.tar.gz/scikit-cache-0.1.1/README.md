# Scikit Cache

Pickle-based caching library. Supports file-system caching only.

## Installation

```
pip install scikit_cache
```

Or to develop package you may install dev dependencies:
```
pip install -e ".[dev]" && pip uninstall -y scikit_cache
```

## How to disable logs

### Option 1: Disable all logs in cache controller

```
from scikit_cache import CacheController

cache = CacheController(..., logger=None)
```

### Option 2: Disable specific logs

To disable specific logs you need to add one of these lines before executing code with cache:

```
import logging

# Disable basic logs like "cache enabled" or "cache disabled"
logging.getLogger('scikit_cache.controller').setLevel(logging.ERROR)

# Disable logs from "@cache.decorator" only
logging.getLogger('scikit_cache.decorator').setLevel(logging.ERROR)

# Disable logs for estimators created by "make_cached_estimator"
logging.getLogger('scikit_cache.estimator').setLevel(logging.ERROR)

# Disable hashing errors
logging.getLogger('scikit_cache.hashing').setLevel(logging.ERROR)
```
