import os
from datetime import datetime
from typing import Union


def set_file_access_time(filename: str, atime: Union[datetime, str]) -> float:
    """Set file access time.

    Set the access time of a given filename to the given atime.
    atime must be a datetime object.
    """
    if isinstance(atime, str):
        atime = datetime.now()

    st_atime = atime.timestamp()
    os.utime(filename, times=(st_atime, os.stat(filename).st_mtime))
    return st_atime


def get_file_access_time(filename: str) -> float:
    """Get file access time.

    :param filename: file path
    :return: timestamp as float
    """
    return os.stat(filename).st_atime
