from ctypes import *

ARCHIVE_WRITE_CALLBACK = CFUNCTYPE(c_ssize_t, c_void_p, c_void_p, c_void_p, c_size_t)
ARCHIVE_OPEN_CALLBACK = CFUNCTYPE(c_int, c_void_p, c_void_p)
ARCHIVE_CLOSE_CALLBACK = CFUNCTYPE(c_int, c_void_p, c_void_p)
