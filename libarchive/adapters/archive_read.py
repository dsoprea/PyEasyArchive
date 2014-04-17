import contextlib
import ctypes
import logging

import libarchive.constants.archive
import libarchive.exception
import libarchive.calls.archive_read
import libarchive.calls.archive_write
import libarchive.calls.archive_general
import libarchive.adapters.archive_entry

from libarchive.calls.archive_general import c_archive_error_string

_logger = logging.getLogger(__name__)

def _archive_read_new():
    archive = libarchive.calls.archive_read.c_archive_read_new()
    if archive is None:
        raise ValueError("Could not create archive resource (read_new).")

    return archive

def _archive_read_support_filter_all(archive):
    try:
        return libarchive.calls.archive_read.c_archive_read_support_filter_all(
                archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_read_support_format_all(archive):
    try:
        return libarchive.calls.archive_read.c_archive_read_support_format_all(
                archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_read_support_format_7zip(archive):
    try:
        return libarchive.calls.archive_read.\
                c_archive_read_support_format_7zip(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_read_open_filename(archive, filepath, block_size_bytes):
    try:
        return libarchive.calls.archive_read.c_archive_read_open_filename(
                archive, 
                filepath, 
                block_size_bytes)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

@contextlib.contextmanager
def _archive_read_next_header(archive):
    entry = ctypes.c_void_p()

    r = libarchive.calls.archive_read.c_archive_read_next_header(
            archive, 
            ctypes.byref(entry))

    if r == libarchive.constants.archive.ARCHIVE_OK:
        yield entry
    elif r == libarchive.constants.archive.ARCHIVE_EOF:
        yield None
    else:
        message = c_archive_error_string(archive)
        raise ValueError("Archive iteration (read_next_header) returned "
                         "error: (%d) [%s]" % (r, message))

def _archive_read_data_skip(archive):
    try:
        return libarchive.calls.archive_read.c_archive_read_data_skip(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_read_free(archive):
    try:
        return libarchive.calls.archive_read.c_archive_read_free(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_set_format_7zip(archive):
    try:
        return libarchive.calls.archive_read.c_archive_write_set_format_7zip(
                archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)



def _archive_read_disk_new():
    archive = libarchive.calls.archive_read.c_archive_read_disk_new()
    if archive is None:
        raise ValueError("Could not create archive resource (read_disk_new).")

    return archive

def _archive_read_disk_set_standard_lookup(archive):
    try:
        return libarchive.calls.archive_read.\
                c_archive_read_disk_set_standard_lookup(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_read_disk_open(archive, filepath):
    try:
        return libarchive.calls.archive_read.c_archive_read_disk_open(
                archive, filepath)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_read_next_header2(archive, entry):
    r = libarchive.calls.archive_read.c_archive_read_next_header2(
            archive, 
            entry)

    if r not in (libarchive.constants.archive.ARCHIVE_OK,
                 libarchive.constants.archive.ARCHIVE_EOF):
        message = c_archive_error_string(archive)
        raise ValueError("Archive iteration (read_next_header2) returned "
                         "error: (%d) [%s]" % (r, message))
    
    return r

def _archive_read_disk_descend(archive):
    try:
        return libarchive.calls.archive_read.c_archive_read_disk_descend(
                archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

_READ_FILTER_MAP = {
        'all': _archive_read_support_filter_all,
    }

_READ_FORMAT_MAP = {
        'all': _archive_read_support_format_all,
        '7z': _archive_read_support_format_7zip,
    }

def _set_read_context(archive_res, filter_name, format_name):
    _filter = _READ_FILTER_MAP[filter_name]        
    r = _filter(archive_res)
    _logger.debug("Filter [%s] returned: %d", _filter, r)

    _format = _READ_FORMAT_MAP[format_name]
    r = _format(archive_res)
    _logger.debug("Format [%s] returned: %d", _format, r)

@contextlib.contextmanager
def reader(filepath, 
           entry_cls=libarchive.adapters.archive_entry.ArchiveEntry, 
           block_size=10240, 
           filter_name='all', 
           format_name='all'):
    """Get a generator with which to enumerate the entries."""

    _logger.info("Reading through archive: %s", filepath)

    archive_res = _archive_read_new()
    _logger.debug("Created archive resource (archive_read_new).")

    try:
        r = _set_read_context(archive_res, filter_name, format_name)

        r = _archive_read_open_filename(archive_res, filepath, block_size)
        _logger.debug("archive_read_open_filename: (%d) %s", r, filepath)

        def it():
            while 1:
                with _archive_read_next_header(archive_res) as entry_res:
                    if entry_res is None:
                        break

                    yield entry_cls(archive_res, entry_res)
                    _archive_read_data_skip(archive_res)

        yield it()
    finally:
        _archive_read_free(archive_res)


class ArchiveEntryItState(libarchive.adapters.archive_entry.ArchiveEntry):
    def __init__(self, *args, **kwargs):
        super(ArchiveEntryItState, self).__init__(*args, **kwargs)
        self.__selected = True

    def set_selected(self, selected=True):
        self.__selected = selected

    @property
    def selected(self):
        return self.__selected

def pour(filepath, flags=0, *args, **kwargs):
    """Write the archive out to the current directory."""

    _logger.info("Pouring archive: %s", filepath)

    with reader(filepath, *args, entry_cls=ArchiveEntryItState, **kwargs) as r:
        ext = libarchive.calls.archive_write.c_archive_write_disk_new()
        libarchive.calls.archive_write.c_archive_write_disk_set_options(
                ext,
                flags
            )

        for state in r:
            yield state

            if state.selected is False:
                continue

            r = libarchive.calls.archive_write.c_archive_write_header(
                    ext, 
                    state.entry_res)

            buff = ctypes.c_void_p()
            size = ctypes.c_size_t()
            offset = ctypes.c_longlong()

            while 1:
                r = libarchive.calls.archive_read.\
                        c_archive_read_data_block(
                            state.reader_res, 
                            ctypes.byref(buff), 
                            ctypes.byref(size), 
                            ctypes.byref(offset))

                if r == libarchive.constants.archive.ARCHIVE_EOF:
                    break
                elif r != libarchive.constants.archive.ARCHIVE_OK:
                    raise ValueError("Pour failed: %d" % (r))

                r = libarchive.calls.archive_write.c_archive_write_data_block(
                        ext, 
                        buff, 
                        size, 
                        offset)

            r = libarchive.calls.archive_write.\
                    c_archive_write_finish_entry(ext)
