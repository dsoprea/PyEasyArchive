from __future__ import division, print_function, unicode_literals

from contextlib import contextmanager
from ctypes import byref, c_longlong, c_size_t, c_void_p

from .ffi import (
    write_disk_new, write_disk_set_options, write_free, write_header,
    read_data_block, write_data_block, write_finish_entry, ARCHIVE_EOF
)
from .read import file_reader, memory_reader


@contextmanager
def new_archive_write_disk(flags):
    archive_p = write_disk_new()
    write_disk_set_options(archive_p, flags)
    try:
        yield archive_p
    finally:
        write_free(archive_p)


def extract_archive(archive, flags=0):
    """Extracts the given archive into the current directory.
    """
    read_p = archive._pointer
    buff, size, offset = c_void_p(), c_size_t(), c_longlong()
    buff_p, size_p, offset_p = byref(buff), byref(size), byref(offset)
    with new_archive_write_disk(flags) as write_p:
        for entry in archive:
            write_header(write_p, entry._entry_p)
            while 1:
                r = read_data_block(read_p, buff_p, size_p, offset_p)
                if r == ARCHIVE_EOF:
                    break
                write_data_block(write_p, buff, size, offset)
            write_finish_entry(write_p)


def extract_entries(entries, flags=0):
    """Extracts the given archive entries into the current directory.
    """
    buff, size, offset = c_void_p(), c_size_t(), c_longlong()
    buff_p, size_p, offset_p = byref(buff), byref(size), byref(offset)
    with new_archive_write_disk(flags) as write_p:
        for entry in entries:
            write_header(write_p, entry._entry_p)
            read_p = entry._archive_p
            while 1:
                r = read_data_block(read_p, buff_p, size_p, offset_p)
                if r == ARCHIVE_EOF:
                    break
                write_data_block(write_p, buff, size, offset)
            write_finish_entry(write_p)


def extract_file(filepath, flags=0):
    """Extracts an archive from a file into the current directory."""
    extract_archive(file_reader(filepath), flags)


def extract_memory(buffer_, flags=0):
    """Extracts an archive from memory into the current directory."""
    extract_archive(memory_reader(buffer_), flags)
