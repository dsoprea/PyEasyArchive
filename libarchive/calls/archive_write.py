from ctypes import *

from libarchive.library import libarchive
from libarchive.types.archive import *
from libarchive.constants.archive import *

def _check_zero_success(value):
    if value != ARCHIVE_OK:
        raise ValueError("Function returned failure: (%d)" % (value))
    
    return value

c_archive_write_disk_new = libarchive.archive_write_disk_new
c_archive_write_disk_new.argtypes = []
c_archive_write_disk_new.restype = c_void_p

c_archive_write_disk_set_options = libarchive.archive_write_disk_set_options
c_archive_write_disk_set_options.argtypes = [c_void_p, c_int]
c_archive_write_disk_set_options.restype = _check_zero_success

c_archive_write_header = libarchive.archive_write_header
c_archive_write_header.argtypes = [c_void_p, c_void_p]
c_archive_write_header.restype = _check_zero_success

c_archive_write_finish_entry = libarchive.archive_write_finish_entry
c_archive_write_finish_entry.argtypes = [c_void_p]
c_archive_write_finish_entry.restype = _check_zero_success

c_archive_write_close = libarchive.archive_write_close
c_archive_write_close.argtypes = [c_void_p]
c_archive_write_close.restype = _check_zero_success

c_archive_write_fail = libarchive.archive_write_fail
c_archive_write_fail.argtypes = [c_void_p]
c_archive_write_fail.restype = _check_zero_success

c_archive_error_string = libarchive.archive_error_string
c_archive_error_string.argtypes = [c_void_p]
c_archive_error_string.restype = c_char_p

c_archive_write_free = libarchive.archive_write_free
c_archive_write_free.argtypes = [c_void_p]
c_archive_write_free.restype = _check_zero_success

c_archive_write_data_block = libarchive.archive_write_data_block
c_archive_write_data_block.argtypes = [
    c_void_p,
    c_void_p,
    c_size_t,
    c_longlong]
c_archive_write_data_block.restype = _check_zero_success

c_archive_write_set_format_7zip = libarchive.archive_write_set_format_7zip
c_archive_write_set_format_7zip.argtypes = [c_void_p]
c_archive_write_set_format_7zip.restype = _check_zero_success

