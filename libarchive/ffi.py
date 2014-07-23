from __future__ import division, print_function, unicode_literals

from ctypes import (
    c_char_p, c_int, c_longlong, c_size_t, c_ssize_t, c_void_p, c_wchar_p,
    pythonapi, CFUNCTYPE, POINTER,
)
import ctypes
import ctypes.util
import logging

from .exception import ArchiveError


page_size = pythonapi.getpagesize()

_logger = logging.getLogger(__name__)

_LIB_FILEPATH = ctypes.util.find_library('libarchive') or 'libarchive.so'
libarchive = ctypes.cdll.LoadLibrary(_LIB_FILEPATH)


ARCHIVE_EOF = 1       # Found end of archive.
ARCHIVE_OK = 0        # Operation was successful.
ARCHIVE_RETRY = -10   # Retry might succeed.
ARCHIVE_WARN = -20    # Partial success.
ARCHIVE_FAILED = -25  # Current operation cannot complete.
ARCHIVE_FATAL = -30   # No more operations are possible.


# Callback types

WRITE_CALLBACK = CFUNCTYPE(
    c_ssize_t, c_void_p, c_void_p, POINTER(c_void_p), c_size_t
)
OPEN_CALLBACK = CFUNCTYPE(c_int, c_void_p, c_void_p)
CLOSE_CALLBACK = CFUNCTYPE(c_int, c_void_p, c_void_p)
VOID_CB = lambda *_: ARCHIVE_OK


# Type aliases, for readability

c_archive_p = c_void_p
c_archive_entry_p = c_void_p


# Helper functions

def archive_error(archive_p):
    raise ArchiveError(error_string(archive_p), errno=errno(archive_p))


def check_null(ret, func, args):
    if ret is None:
        raise ArchiveError(func.__name__+' returned NULL')
    return ret


def check_int(retcode, func, args):
    if retcode >= 0:
        return retcode
    elif retcode == ARCHIVE_WARN:
        _logger.warn(error_string(args[0]))
        return retcode
    else:
        raise archive_error(args[0])


def ffi(name, argtypes, restype, errcheck=None):
    f = getattr(libarchive, 'archive_'+name)
    f.argtypes = argtypes
    f.restype = restype
    if errcheck:
        f.errcheck = errcheck
    globals()[name] = f
    return f


# FFI declarations

# archive_util

errno = ffi('errno', [c_archive_p], c_int)
error_string = ffi('error_string', [c_archive_p], c_char_p)

# archive_entry

ffi('entry_new', [], c_archive_entry_p, check_null)

ffi('entry_mtime', [c_archive_entry_p], c_int)
ffi('entry_pathname_w', [c_archive_entry_p], c_wchar_p)
ffi('entry_sourcepath', [c_archive_entry_p], c_char_p)
ffi('entry_size', [c_archive_entry_p], c_longlong)

ffi('entry_update_pathname_utf8', [c_archive_entry_p, c_char_p], None)

ffi('entry_clear', [c_archive_entry_p], c_archive_entry_p)
ffi('entry_free', [c_archive_entry_p], None)

# archive_read

ffi('read_new', [], c_archive_p, check_null)

ffi('read_support_filter_all', [c_archive_p], c_int, check_int)
ffi('read_support_format_all', [c_archive_p], c_int, check_int)
ffi('read_support_format_7zip', [c_archive_p], c_int, check_int)

ffi('read_open_filename', [c_archive_p, c_char_p, c_size_t], c_int, check_int)
ffi('read_open_filename_w', [c_archive_p, c_wchar_p, c_size_t],
    c_int, check_int)
ffi('read_open_memory', [c_archive_p, c_void_p, c_size_t], c_int, check_int)

ffi('read_next_header', [c_archive_p, POINTER(c_void_p)], c_int, check_int)
ffi('read_next_header2', [c_archive_p, c_void_p], c_int, check_int)

ffi('read_close', [c_archive_p], c_int, check_int)
ffi('read_free', [c_archive_p], c_int, check_int)

# archive_read_disk

ffi('read_disk_new', [], c_archive_p, check_null)
ffi('read_disk_set_standard_lookup', [c_archive_p], c_int, check_int)
ffi('read_disk_open', [c_archive_p, c_char_p], c_int, check_int)
ffi('read_disk_open_w', [c_archive_p, c_wchar_p], c_int, check_int)
ffi('read_disk_descend', [c_archive_p], c_int, check_int)

# archive_read_data

ffi('read_data_block',
    [c_archive_p, POINTER(c_void_p), POINTER(c_size_t), POINTER(c_longlong)],
    c_int, check_int)
ffi('read_data', [c_archive_p, c_void_p, c_size_t], c_ssize_t, check_int)
ffi('read_data_skip', [c_archive_p], c_int, check_int)

# archive_write

ffi('write_new', [], c_archive_p, check_null)

ffi('write_disk_new', [], c_archive_p, check_null)
ffi('write_disk_set_options', [c_archive_p, c_int], c_int, check_int)

ffi('write_set_format_7zip', [c_archive_p], c_int, check_int)
ffi('write_set_format_ustar', [c_archive_p], c_int, check_int)

ffi('write_add_filter_bzip2', [c_archive_p], c_int, check_int)
ffi('write_add_filter_compress', [c_archive_p], c_int, check_int)
ffi('write_add_filter_gzip', [c_archive_p], c_int, check_int)
ffi('write_add_filter_none', [c_archive_p], c_int, check_int)

ffi('write_open',
    [c_archive_p, c_void_p, OPEN_CALLBACK, WRITE_CALLBACK, CLOSE_CALLBACK],
    c_int, check_int)
ffi('write_open_fd', [c_archive_p, c_int], c_int, check_int)
ffi('write_open_filename', [c_archive_p, c_char_p], c_int, check_int)
ffi('write_open_filename_w', [c_archive_p, c_wchar_p], c_int, check_int)
ffi('write_open_memory',
    [c_archive_p, c_void_p, c_size_t, POINTER(c_size_t)],
    c_int, check_int)

ffi('write_get_bytes_in_last_block', [c_archive_p], c_int, check_int)
ffi('write_get_bytes_per_block', [c_archive_p], c_int, check_int)
ffi('write_set_bytes_in_last_block', [c_archive_p, c_int], c_int, check_int)
ffi('write_set_bytes_per_block', [c_archive_p, c_int], c_int, check_int)

ffi('write_header', [c_archive_p, c_void_p], c_int, check_int)
ffi('write_data', [c_archive_p, c_void_p, c_size_t], c_ssize_t, check_int)
ffi('write_data_block', [c_archive_p, c_void_p, c_size_t, c_longlong],
    c_int, check_int)
ffi('write_finish_entry', [c_archive_p], c_int, check_int)

ffi('write_close', [c_archive_p], c_int, check_int)
ffi('write_free', [c_archive_p], c_int, check_int)
