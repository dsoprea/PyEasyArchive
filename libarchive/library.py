import ctypes
import ctypes.util
import logging

_logger = logging.getLogger(__name__)

_LIB_FILEPATH = ctypes.util.find_library('libarchive')
if _LIB_FILEPATH is None:
    _LIB_FILEPATH = 'libarchive.so'
    _logger.debug("Could not use find_library to find library. Defaulting to "
                  "'%s'." % (_LIB_FILEPATH))
else:
    _logger.debug("find_library rendered '%s'." % (_LIB_FILEPATH))

libarchive = ctypes.cdll.LoadLibrary(_LIB_FILEPATH)
