from ctypes import *

from libarchive.library import libarchive
from libarchive.constants.archive import *

def _check_zero_success(value):
    if value != ARCHIVE_OK:
        raise ValueError("Function returned failure: (%d)" % (value))
    
    return value

c_archive_read_support_format_all = libarchive.archive_read_support_format_all
c_archive_read_support_format_all.argtypes = [c_void_p]
c_archive_read_support_format_all.restype = _check_zero_success
