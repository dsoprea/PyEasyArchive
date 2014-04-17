import ctypes
import ctypes.util

_LIB_FILEPATH = ctypes.util.find_library('libarchive')
if _LIB_FILEPATH is None:
    _LIB_FILEPATH = 'libarchive.so'

libarchive = ctypes.cdll.LoadLibrary(_LIB_FILEPATH)

