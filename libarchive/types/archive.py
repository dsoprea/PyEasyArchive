from ctypes import *

try:
    from ctypes import c_ssize_t
except ImportError:
    from ctypes import c_longlong as c_ssize_t

ARCHIVE_WRITE_CALLBACK = CFUNCTYPE(c_ssize_t, c_void_p, c_void_p, POINTER(c_void_p), c_size_t)
ARCHIVE_OPEN_CALLBACK = CFUNCTYPE(c_int, c_void_p, c_void_p)
ARCHIVE_CLOSE_CALLBACK = CFUNCTYPE(c_int, c_void_p, c_void_p)
