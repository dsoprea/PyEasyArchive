from ctypes import *

from libarchive.library import libarchive
from libarchive.types.archive import *
from libarchive.constants.archive import *

def _check_zero_success(value):
    if value != ARCHIVE_OK:
        raise ValueError("Function returned failure: (%d)" % (value))
    
    return value

c_archive_entry_pathname = libarchive.archive_entry_pathname
c_archive_entry_pathname.argtypes = [c_void_p]
c_archive_entry_pathname.restype = c_char_p

c_archive_entry_new = libarchive.archive_entry_new
c_archive_entry_new.argtypes = []
c_archive_entry_new.restype = c_void_p

c_archive_entry_sourcepath = libarchive.archive_entry_sourcepath
c_archive_entry_sourcepath.argtypes = [c_void_p]
c_archive_entry_sourcepath.restype = _check_zero_success

c_archive_entry_free = libarchive.archive_entry_free
c_archive_entry_free.argtypes = [c_void_p]
c_archive_entry_free.restype = None

