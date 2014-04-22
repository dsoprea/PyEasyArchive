import sys
import ctypes
import logging

import libarchive.constants.archive
import libarchive.exception
import libarchive.calls.archive_write
import libarchive.calls.archive_read
import libarchive.adapters.archive_entry

from libarchive.calls.archive_general import c_archive_error_string

_logger = logging.getLogger(__name__)

def _archive_write_new():
    archive = libarchive.calls.archive_write.c_archive_write_new()
    if archive is None:
        raise ValueError("Could not create archive resource (write_new).")

    return archive

def _archive_write_disk_new():
    archive = libarchive.calls.archive_write.c_archive_write_disk_new()
    if archive is None:
        raise ValueError("Could not create archive resource (write_disk_new).")

    return archive

def _archive_write_disk_set_options(archive, flags):
    try:
        libarchive.calls.archive_write.c_archive_write_disk_set_options(
            archive, 
            flags)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_finish_entry(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_finish_entry(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_close(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_close(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

#def _archive_write_fail(archive):
#    try:
#        libarchive.calls.archive_write.c_archive_write_fail(archive)
#    except:
#        message = c_archive_error_string(archive)
#        raise libarchive.exception.ArchiveError(message)

def _archive_write_free(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_free(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_data(archive, data):
    n = libarchive.calls.archive_write.c_archive_write_data(
            archive, 
            ctypes.cast(ctypes.c_char_p(data), ctypes.c_void_p), 
            len(data))

    if n == 0:
        message = c_archive_error_string(archive)
        raise ValueError("No bytes were written. Error? [%s]" % (message))


def _archive_write_set_format_7zip(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_set_format_7zip(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)



def _archive_write_add_filter_bzip2(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_add_filter_bzip2(
            archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_add_filter_compress(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_add_filter_compress(
            archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_add_filter_gzip(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_add_filter_gzip(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_add_filter_none(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_add_filter_none(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_set_format_ustar(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_set_format_ustar(
            archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_open_filename(archive, filepath):
    try:
        libarchive.calls.archive_write.c_archive_write_open_filename(
            archive, 
            filepath)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_header(archive, entry):
    try:
        return libarchive.calls.archive_write.c_archive_write_header(
                archive, 
                entry)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_read_disk_set_standard_lookup(archive):
    try:
        libarchive.calls.archive_write.c_archive_read_disk_set_standard_lookup(
            archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_open_memory(archive, buffer, counter):
    try:
        libarchive.calls.archive_write.c_archive_write_open_memory(
            archive,
            ctypes.cast(ctypes.c_char_p(buffer), ctypes.c_void_p), 
            len(buffer), 
            ctypes.byref(counter))
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_open_fd(archive, stream=sys.stdout):
    fp = stream.fileno()

    try:
        return libarchive.calls.archive_write.c_archive_write_open_fd(archive, fp)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

_WRITE_FILTER_MAP = {
        None:       _archive_write_add_filter_none,
        'bz2':      _archive_write_add_filter_bzip2,
        'compress': _archive_write_add_filter_compress,
        'gz':       _archive_write_add_filter_gzip,
    }

_WRITE_FORMAT_MAP = {
        'ustar': _archive_write_set_format_ustar,
        '7z':    _archive_write_set_format_7zip,
    }

def create(format_name, files, filepath=None, filter_name=None, buffer_length=16384):
    """Create an archive from a collection of files (not recursive)."""

    _logger.debug("Creating archive with format [%s] from (%d) files: "
                  "NAME=[%s]", 
                  format_name, len(files), filepath)

    format_ = _WRITE_FORMAT_MAP[format_name]
    filter_ = _WRITE_FILTER_MAP[filter_name]

    a = _archive_write_new()
    filter_(a)
    format_(a)

# TODO(dustin): Allow for the following output modes:
# 1. stdout (_archive_write_open_fd)
# 2. file: (_archive_write_open_filename)
# 3. memory (_archive_write_open_memory)
    if filepath is not None:
        _archive_write_open_filename(a, filepath)
    else:
        _archive_write_open_fd(a)

# Use the standard uid/gid lookup mechanisms.
# This was set on an instance of *disk* that wasn't used. Do we still need it?
#_archive_read_disk_set_standard_lookup(disk)

    for filepath in files:
        disk = libarchive.calls.archive_read.c_archive_read_disk_new()
        libarchive.calls.archive_read.c_archive_read_disk_open(
            disk, 
            filepath)

        while 1:
            entry = libarchive.calls.archive_entry.c_archive_entry_new()
            r = libarchive.calls.archive_read.c_archive_read_next_header2(
                    disk, 
                    entry)

            if r == libarchive.constants.archive.ARCHIVE_EOF:
                break
            elif r != libarchive.constants.archive.ARCHIVE_OK:
                message = c_archive_error_string(disk)
                raise libarchive.exception.ArchiveError(
                        "Create failed: (%d) [%s]" % (r, message))

            wrapped = libarchive.adapters.archive_entry.ArchiveEntry(
                        disk, 
                        entry)

            yield wrapped

            libarchive.calls.archive_read.c_archive_read_disk_descend(disk)

            r = _archive_write_header(a, entry)

            with open(wrapped.sourcepath, 'rb') as f:
                while 1:
                    data = f.read(buffer_length)
                    if not data:
                        break

                    _archive_write_data(a, data)

            libarchive.calls.archive_entry.c_archive_entry_free(entry)

        libarchive.calls.archive_read.c_archive_read_close(disk)
        libarchive.calls.archive_read.c_archive_read_free(disk)

    _archive_write_close(a)
    _archive_write_free(a)
