from __future__ import division, print_function, unicode_literals

from contextlib import contextmanager
from ctypes import cast, c_void_p
from os import stat

from . import ffi
from .ffi import ARCHIVE_EOF
from .entry import ArchiveEntry, new_archive_entry


class ArchiveRead(object):

    def __init__(self, archive_p):
        self._pointer = archive_p

    def __iter__(self):
        """Iterates through an archive's entries.
        """
        archive_p = self._pointer
        read_next_header2 = ffi.read_next_header2
        with new_archive_entry() as entry_p:
            entry = ArchiveEntry(archive_p, entry_p)
            while 1:
                r = read_next_header2(archive_p, entry_p)
                if r == ARCHIVE_EOF:
                    return
                yield entry


@contextmanager
def new_archive_read(filter_name='all', format_name='all'):
    """Creates an archive struct suitable for reading from an archive.

    Returns a pointer if successful. Raises ArchiveError on error.
    """
    archive_p = ffi.read_new()
    getattr(ffi, 'read_support_filter_'+filter_name)(archive_p)
    getattr(ffi, 'read_support_format_'+format_name)(archive_p)
    try:
        yield archive_p
    finally:
        ffi.read_free(archive_p)


@contextmanager
def file_reader(filepath, block_size=4096):
    """Read an archive from a file.
    """
    with new_archive_read() as archive_p:
        try:
            block_size = stat(filepath).st_blksize
        except (OSError, AttributeError):
            pass
        ffi.read_open_filename_w(archive_p, filepath, block_size)
        yield ArchiveRead(archive_p)


@contextmanager
def memory_reader(buffer_):
    """Read an archive from memory.
    """
    with new_archive_read() as archive_p:
        ffi.read_open_memory(cast(buffer_, c_void_p), len(buffer_))
        yield ArchiveRead(archive_p)
