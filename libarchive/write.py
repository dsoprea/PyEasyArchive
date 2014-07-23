from __future__ import division, print_function, unicode_literals

from contextlib import contextmanager
from ctypes import cast, c_char, POINTER

from . import ffi
from .entry import ArchiveEntry, new_archive_entry
from .ffi import (
    OPEN_CALLBACK, WRITE_CALLBACK, CLOSE_CALLBACK, VOID_CB,
    ARCHIVE_EOF, page_size,
    entry_sourcepath, entry_clear,
    read_disk_new, read_disk_open_w, read_next_header2, read_disk_descend,
    read_free, write_header, write_data, write_finish_entry,
)


@contextmanager
def new_archive_read_disk(path):
    archive_p = read_disk_new()
    read_disk_open_w(archive_p, path)
    try:
        yield archive_p
    finally:
        read_free(archive_p)


class ArchiveWrite(object):

    def __init__(self, archive_p):
        self._pointer = archive_p

    def add_entries(self, entries):
        """Add the given entries to the archive.
        """
        write_p = self._pointer
        for entry in entries:
            write_header(write_p, entry._entry_p)
            for block in entry.get_blocks():
                write_data(write_p, block, len(block))
            write_finish_entry(write_p)

    def add_files(self, *paths):
        """Read the given paths from disk and add them to the archive.
        """
        write_p = self._pointer

        block_size = ffi.write_get_bytes_per_block(write_p)
        if block_size <= 0:
            block_size = 10240

        with new_archive_entry() as entry_p:
            entry = ArchiveEntry(None, entry_p)
            for path in paths:
                with new_archive_read_disk(path) as read_p:
                    while 1:
                        r = read_next_header2(read_p, entry_p)
                        if r == ARCHIVE_EOF:
                            break
                        entry.pathname = entry.pathname.lstrip('/')
                        read_disk_descend(read_p)
                        write_header(write_p, entry_p)
                        try:
                            with open(entry_sourcepath(entry_p), 'rb') as f:
                                while 1:
                                    data = f.read(block_size)
                                    if not data:
                                        break
                                    write_data(write_p, data, len(data))
                        except IOError as e:
                            if e.errno != 21:
                                raise
                        write_finish_entry(write_p)
                        entry_clear(entry_p)


@contextmanager
def new_archive_write(format_name=None, filter_name=None):
    archive_p = ffi.write_new()
    if format_name:
        getattr(ffi, 'write_set_format_'+format_name)(archive_p)
    if filter_name:
        getattr(ffi, 'write_add_filter_'+filter_name)(archive_p)
    try:
        yield archive_p
    finally:
        ffi.write_free(archive_p)


@contextmanager
def file_writer(filepath, format_name=None, filter_name=None):
    with new_archive_write(format_name, filter_name) as archive_p:
        ffi.write_open_filename_w(archive_p, filepath)
        yield ArchiveWrite(archive_p)


@contextmanager
def fd_writer(fd, format_name, filter_name=None):
    with new_archive_write(format_name, filter_name) as archive_p:
        ffi.write_open_fd(archive_p, fd)
        yield ArchiveWrite(archive_p)


@contextmanager
def custom_writer(write_cb, format_name=None, filter_name=None,
                  open_cb=VOID_CB, close_cb=VOID_CB, block_size=page_size):

    def write_cb_internal(archive_p, context, buffer_, length):
        data = cast(buffer_, POINTER(c_char * length))[0]
        return write_cb(data, length)

    with new_archive_write(format_name, filter_name) as archive_p:
        ffi.write_set_bytes_in_last_block(archive_p, 1)
        ffi.write_set_bytes_per_block(archive_p, block_size)
        ffi.write_open(
            archive_p,
            None,
            OPEN_CALLBACK(open_cb),
            WRITE_CALLBACK(write_cb_internal),
            CLOSE_CALLBACK(close_cb)
        )
        yield ArchiveWrite(archive_p)
