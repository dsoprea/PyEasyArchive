from ctypes import *

from libarchive.library import libarchive

c_archive_error_string = libarchive.archive_error_string
c_archive_error_string.argtypes = [c_void_p]
c_archive_error_string.restype = c_char_p

def get_error_string(archive, decode=True):
    b = c_archive_error_string(archive)

    if decode is True:
        return b.decode('utf-8')
    else:
        return b
