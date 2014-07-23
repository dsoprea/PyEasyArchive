from ctypes import *

from libarchive.library import libarchive

def _check_zero_success(value):
    if value != ARCHIVE_OK:
        raise ValueError("Function returned failure: (%d)" % (value))
    
    return value

c_archive_write_set_format = libarchive.archive_write_set_format
c_archive_write_set_format.argtypes = [c_void_p, c_int]
c_archive_write_set_format.restype = _check_zero_success
