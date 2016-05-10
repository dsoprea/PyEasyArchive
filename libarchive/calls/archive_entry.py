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

c_archive_entry_set_pathname = libarchive.archive_entry_set_pathname
c_archive_entry_set_pathname.argtypes = [c_void_p, c_char_p]
c_archive_entry_set_pathname.restype = None

c_archive_entry_filetype = libarchive.archive_entry_filetype
c_archive_entry_filetype.argtypes = [c_void_p]
c_archive_entry_filetype.restype = c_int

c_archive_entry_mtime = libarchive.archive_entry_mtime
c_archive_entry_mtime.argtypes = [c_void_p]
c_archive_entry_mtime.restype = c_long

c_archive_entry_perm = libarchive.archive_entry_perm
c_archive_entry_perm.argtypes = [c_void_p]
c_archive_entry_perm.restype = c_int
