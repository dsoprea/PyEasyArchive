import logging
import os

import ctypes
import ctypes.util

_logger = logging.getLogger(__name__)

_FILEPATH = os.environ.get('LA_LIBRARY_FILEPATH', '')
if _FILEPATH == '':
    _FILEPATH = ctypes.util.find_library('libarchive')
    if _FILEPATH is None:
        _FILEPATH = 'libarchive.so'

_logger.debug("Using library: [%s]", _FILEPATH)
libarchive = ctypes.cdll.LoadLibrary(_FILEPATH)
