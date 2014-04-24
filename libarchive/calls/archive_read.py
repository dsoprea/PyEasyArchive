from ctypes import *

from libarchive.library import libarchive
from libarchive.types.archive import *
from libarchive.constants.archive import *

def _check_zero_success(value):
    if value != ARCHIVE_OK:
        raise ValueError("Function returned failure: (%d)" % (value))
    
    return value

c_archive_read_new = libarchive.archive_read_new
c_archive_read_new.argtypes = []
c_archive_read_new.restype = c_void_p

c_archive_read_support_filter_all = libarchive.archive_read_support_filter_all
c_archive_read_support_filter_all.argtypes = [c_void_p]
c_archive_read_support_filter_all.restype = _check_zero_success

c_archive_read_support_format_all = libarchive.archive_read_support_format_all
c_archive_read_support_format_all.argtypes = [c_void_p]
c_archive_read_support_format_all.restype = _check_zero_success

c_archive_read_support_format_7zip = \
    libarchive.archive_read_support_format_7zip
c_archive_read_support_format_7zip.argtypes = [c_void_p]
c_archive_read_support_format_7zip.restype = _check_zero_success

c_archive_read_open_filename = libarchive.archive_read_open_filename
c_archive_read_open_filename.argtypes = [c_void_p, c_char_p, c_size_t]
c_archive_read_open_filename.restype = _check_zero_success

c_archive_read_open_memory = libarchive.archive_read_open_memory
c_archive_read_open_memory.argtypes = [c_void_p, c_void_p, c_size_t]
c_archive_read_open_memory.restype = _check_zero_success

c_archive_read_next_header = libarchive.archive_read_next_header
c_archive_read_next_header.argtypes = [c_void_p, POINTER(c_void_p)]
c_archive_read_next_header.restype = c_int

c_archive_read_data_skip = libarchive.archive_read_data_skip
c_archive_read_data_skip.argtypes = [c_void_p]
c_archive_read_data_skip.restype = _check_zero_success

c_archive_read_free = libarchive.archive_read_free
c_archive_read_free.argtypes = [c_void_p]
c_archive_read_free.restype = _check_zero_success

c_archive_read_data_block = libarchive.archive_read_data_block
c_archive_read_data_block.argtypes = [
    c_void_p, 
    POINTER(c_void_p), 
    POINTER(c_size_t), 
    POINTER(c_longlong)]
c_archive_read_data_block.restype = c_int



c_archive_read_disk_new = libarchive.archive_read_disk_new
c_archive_read_disk_new.argtypes = []
c_archive_read_disk_new.restype = c_void_p

c_archive_read_disk_set_standard_lookup = \
    libarchive.archive_read_disk_set_standard_lookup
c_archive_read_disk_set_standard_lookup.argtypes = [c_void_p]
c_archive_read_disk_set_standard_lookup.restype = _check_zero_success

c_archive_read_disk_open = libarchive.archive_read_disk_open
c_archive_read_disk_open.argtypes = [c_void_p, c_char_p]
c_archive_read_disk_open.restype = _check_zero_success

c_archive_read_next_header2 = libarchive.archive_read_next_header2
c_archive_read_next_header2.argtypes = [c_void_p, c_void_p]
c_archive_read_next_header2.restype = c_int

c_archive_read_disk_descend = libarchive.archive_read_disk_descend
c_archive_read_disk_descend.argtypes = [c_void_p]
c_archive_read_disk_descend.restype = c_int

c_archive_read_close = libarchive.archive_read_close
c_archive_read_close.argtypes = [c_void_p]
c_archive_read_close.restype = _check_zero_success

c_archive_read_data = libarchive.archive_read_data
c_archive_read_data.argtypes = [c_void_p, c_void_p, c_size_t]
c_archive_read_data.restype = c_ssize_t

c_archive_read_data_block = libarchive.archive_read_data_block
c_archive_read_data_block.argtypes = [c_void_p, POINTER(c_void_p), POINTER(c_size_t), POINTER(c_longlong)]
c_archive_read_data_block.restype = c_int
