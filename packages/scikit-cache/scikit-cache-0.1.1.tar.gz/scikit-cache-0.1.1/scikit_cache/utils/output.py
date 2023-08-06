from typing import Optional

COLORS = {
    'blue': ('\x1b[34m\x1b[22m', '\x1b[39m\x1b[22m'),  # blue
    'green': ('\x1b[32m\x1b[22m', '\x1b[39m\x1b[22m'),  # green
    'red': ('\x1b[31m\x1b[22m', '\x1b[39m\x1b[22m'),  # red
    'yellow': ('\x1b[33m\x1b[22m', '\x1b[39m\x1b[22m'),  # yellow
}
COLOR_TO_LEVEL = {
    'info': None,
    'debug': None,
    'warning': 'yellow',
    'error': 'red',
    'exception': 'red',
}


def color_msg(msg: str, color: Optional[str] = None) -> str:
    """Return colored message."""
    if not color or color not in COLORS:
        return msg

    return COLORS[color][0] + msg + COLORS[color][1]


def color_from_level(level: str) -> Optional[str]:
    return COLOR_TO_LEVEL[level]
