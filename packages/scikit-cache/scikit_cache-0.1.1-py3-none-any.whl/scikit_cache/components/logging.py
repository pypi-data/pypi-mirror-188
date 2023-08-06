from logging import Logger
from typing import (
    Callable,
    Optional,
)

from scikit_cache.utils import (
    color_from_level,
    color_msg,
    get_func_name,
)


class LoggingMixin:
    """Mixin for ``CacheController`` class with logging methods."""

    def _log(
        self,
        msg: str,
        level: str = 'info',
        color: Optional[str] = None,
        func: Optional[Callable] = None,
        logger: Optional[Logger] = None,
    ) -> None:
        """Log message.

        Depending on "cache.logger" attribute this method will log using:
            - ``print()`` function
            - ``logging.Logger`` instance
            - No logs at all

        :param msg: log message
        :param level: log level (info, error, warning) if logging via ``logging.Logger``
        :param color: color for print() output (blue, green, red, yellow)
        :param func: include function name in log
        :param logger: ``logging.Logger`` instance to use if logging to logger is enabled
        :return:
        """
        if self.logger is None:
            return

        msg = ' - '.join(filter(bool, (get_func_name(func) if func else None, msg)))  # type: ignore

        if self.logger == 'print':
            color = color or color_from_level(level)
            print(color_msg(msg, color=color))  # noqa
        elif self.logger == 'logger' and logger is not None:
            getattr(logger, level)(msg)
        else:
            raise TypeError(f'Unknown logger type: {self.logger}. Allowed "logger" or "print".')
