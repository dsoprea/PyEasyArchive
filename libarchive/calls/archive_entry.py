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
c_archive_entry_sourcepath.restype = c_char_p

c_archive_entry_free = libarchive.archive_entry_free
c_archive_entry_free.argtypes = [c_void_p]
c_archive_entry_free.restype = None

c_archive_entry_size = libarchive.archive_entry_size
c_archive_entry_size.argtypes = [c_void_p]
c_archive_entry_size.restype = c_longlong

# TODO(dustin): We're still not sure whether we should be using 
#               archive_entry_set_pathname or archive_entry_copy_pathname. 
#               Their internal logic is identical.
c_archive_entry_set_pathname = libarchive.archive_entry_set_pathname
c_archive_entry_set_pathname.argtypes = [c_void_p, c_char_p]
c_archive_entry_set_pathname.restype = None
