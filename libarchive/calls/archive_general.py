import ctypes

c_archive_error_string = libarchive.archive_error_string
c_archive_error_string.argtypes = [ctypes.c_void_p]
c_archive_error_string.restype = ctypes.c_char_p

