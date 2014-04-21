from ctypes import *

from libarchive.library import libarchive
from libarchive.types.archive import *
from libarchive.constants.archive import *

def _check_zero_success(value):
    if value != ARCHIVE_OK:
        raise ValueError("Function returned failure: (%d)" % (value))
    
    return value

c_archive_write_new = libarchive.archive_write_new
c_archive_write_new.argtypes = []
c_archive_write_new.restype = c_void_p

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

#Not supported until 3.1.0 . We don't want to impose it.
#c_archive_write_fail = libarchive.archive_write_fail
#c_archive_write_fail.argtypes = [c_void_p]
#c_archive_write_fail.restype = _check_zero_success

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


c_archive_write_add_filter_bzip2 = libarchive.archive_write_add_filter_bzip2
c_archive_write_add_filter_bzip2.argtypes = [c_void_p]
c_archive_write_add_filter_bzip2.restype = _check_zero_success

c_archive_write_add_filter_compress = \
    libarchive.archive_write_add_filter_compress
c_archive_write_add_filter_compress.argtypes = [c_void_p]
c_archive_write_add_filter_compress.restype = _check_zero_success

c_archive_write_add_filter_gzip = libarchive.archive_write_add_filter_gzip
c_archive_write_add_filter_gzip.argtypes = [c_void_p]
c_archive_write_add_filter_gzip.restype = _check_zero_success

c_archive_write_add_filter_none = libarchive.archive_write_add_filter_none
c_archive_write_add_filter_none.argtypes = [c_void_p]
c_archive_write_add_filter_none.restype = _check_zero_success

c_archive_write_set_format_ustar = libarchive.archive_write_set_format_ustar
c_archive_write_set_format_ustar.argtypes = [c_void_p]
c_archive_write_set_format_ustar.restype = _check_zero_success

c_archive_write_open_filename = libarchive.archive_write_open_filename
c_archive_write_open_filename.argtypes = [c_void_p, c_char_p]
c_archive_write_open_filename.restype = _check_zero_success

c_archive_write_data = libarchive.archive_write_data
c_archive_write_data.argtypes = [c_void_p, c_void_p, c_size_t]
c_archive_write_data.restype = c_ssize_t

c_archive_read_disk_set_standard_lookup = \
    libarchive.archive_read_disk_set_standard_lookup
c_archive_read_disk_set_standard_lookup.argtypes = [c_void_p]
c_archive_read_disk_set_standard_lookup.restype = _check_zero_success

c_archive_write_open_memory = libarchive.archive_write_open_memory
c_archive_write_open_memory.argtypes = [c_void_p, 
                                        c_void_p, 
                                        c_size_t, 
                                        POINTER(c_size_t)]
c_archive_write_open_memory.restype = _check_zero_success

c_archive_write_open_fd = libarchive.archive_write_open_fd
c_archive_write_open_fd.argtypes = [c_void_p, c_int]
c_archive_write_open_fd.restype = _check_zero_success
