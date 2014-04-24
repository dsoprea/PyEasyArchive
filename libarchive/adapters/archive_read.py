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

# TODO(dustin): We might have to switch most of our c_char_p references to 
#               POINTER(c_char), since we're often not using zero-terminated 
#               strings.

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

def _archive_read_open_memory(archive, buffer_):
    libarchive.calls.archive_read.c_archive_read_open_memory(
        archive, 
        ctypes.cast(ctypes.c_char_p(buffer_), ctypes.c_void_p), 
        len(buffer_))

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

# TODO(dustin): We might have to free "entry".


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
    result = libarchive.calls.archive_read.c_archive_read_disk_descend(
                archive)

    if result not in (libarchive.constants.archive.ARCHIVE_OK,
                      libarchive.constants.archive.ARCHIVE_WARN):
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_read_close(archive):
    try:
        return libarchive.calls.archive_read.c_archive_read_close(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_read_data(archive, block_size=8192):
    buffer_ = ctypes.create_string_buffer(block_size)

    while 1:
        num = libarchive.calls.archive_read.c_archive_read_data(
                archive, 
                buffer_.raw, 
                len(buffer_))

        if num == 0:
            break
        elif num < 0:
            message = c_archive_error_string(archive)
            raise libarchive.exception.ArchiveError(message)

        yield buffer_.value[0:num.value]

def _read_by_block(archive_res):
    buffer_ = ctypes.c_char_p()
    num = ctypes.c_size_t()
    offset = ctypes.c_longlong()

    while 1:
        r = libarchive.calls.archive_read.c_archive_read_data_block(
                archive_res, 
                ctypes.cast(ctypes.byref(buffer_), 
                            ctypes.POINTER(ctypes.c_void_p)), 
                ctypes.byref(num), 
                ctypes.byref(offset))

        if r == libarchive.constants.archive.ARCHIVE_OK:
            yield buffer_.value[0:num.value]
        elif r == libarchive.constants.archive.ARCHIVE_EOF:
            break


class _ArchiveEntryItReadable(libarchive.adapters.archive_entry.ArchiveEntry):
    def __init__(self, *args, **kwargs):
        super(_ArchiveEntryItReadable, self).__init__(*args, **kwargs)
        self.__is_consumed = False

    def get_blocks(self):
        for block in _read_by_block(self.reader_res):
            yield block

        self.__is_consumed = True

    @property
    def is_consumed(self):
        return self.__is_consumed


class _ArchiveEntryItState(_ArchiveEntryItReadable):
    def __init__(self, *args, **kwargs):
        super(_ArchiveEntryItState, self).__init__(*args, **kwargs)
        self.__selected = True

    def set_selected(self, selected=True):
        self.__selected = selected

    @property
    def selected(self):
        return self.__selected

_READ_FILTER_MAP = {
        'all': _archive_read_support_filter_all,
    }

_READ_FORMAT_MAP = {
        'all': _archive_read_support_format_all,
        '7z': _archive_read_support_format_7zip,
    }

def _set_read_context(archive_res, filter_name, format_name):
    filter_ = _READ_FILTER_MAP[filter_name]        
    _logger.debug("Invoking filter: %s", filter_.__name__)
    r = filter_(archive_res)

    format = _READ_FORMAT_MAP[format_name]
    _logger.debug("Invoking format: %s", format.__name__)
    r = format(archive_res)

@contextlib.contextmanager
def _enumerator(opener, entry_cls, filter_name='all', format_name='all'):
    """Return an archive enumerator from a user-defined source, using a user-
    defined entry type.
    """

    archive_res = _archive_read_new()

    try:
        r = _set_read_context(archive_res, filter_name, format_name)
        opener(archive_res)

        def it():
            while 1:
                with _archive_read_next_header(archive_res) as entry_res:
                    if entry_res is None:
                        break

                    e = entry_cls(archive_res, entry_res)
                    yield e
                    if e.is_consumed is False:
                        _archive_read_data_skip(archive_res)
        yield it()
    finally:
        _archive_read_free(archive_res)

def file_enumerator(filepath, block_size=10240, *args, **kwargs):
    """Return an enumerator that knows how to read a physical file."""

    _logger.debug("Enumerating through archive file: %s", filepath)

    def opener(archive_res):
        _logger.debug("Opening from file (file_enumerator): %s", filepath)
        _archive_read_open_filename(archive_res, filepath, block_size)

    if 'entry_cls' not in kwargs:
        kwargs['entry_cls'] = _ArchiveEntryItReadable

    return _enumerator(opener, 
                       *args, 
                       **kwargs)

def memory_enumerator(buffer_, *args, **kwargs):
    """Return an enumerator that knows how to read raw memory."""

    _logger.debug("Enumerating through (%d) bytes of archive data.", 
                  len(buffer_))

    def opener(archive_res):
        _logger.debug("Opening from (%d) bytes (memory_enumerator).", 
                      len(buffer_))

        _archive_read_open_memory(archive_res, buffer_)

    if 'entry_cls' not in kwargs:
        kwargs['entry_cls'] = _ArchiveEntryItReadable

    return _enumerator(opener, 
                       *args, 
                       **kwargs)

def file_reader(*args, **kwargs):
    """Return an enumerator that knows how to read the data for entries from a 
    physical file.
    """

    return file_enumerator(*args, 
                           entry_cls=_ArchiveEntryItReadable, 
                           **kwargs)

def memory_reader(*args, **kwargs):
    """Return an enumerator that knows how to read the data for entries from
    memory.
    """

    return memory_enumerator(*args, 
                             entry_cls=_ArchiveEntryItReadable, 
                             **kwargs)

def _pour(opener, flags=0, *args, **kwargs):
    """A flexible pouring facility that knows how to enumerate entry data."""

    with _enumerator(opener, 
                     *args, 
                     entry_cls=_ArchiveEntryItState, 
                     **kwargs) as r:
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
                    message = c_archive_error_string(state.reader_res)
                    raise libarchive.exception.ArchiveError(
                            "Pour failed: (%d) [%s]" % (r, message))

                r = libarchive.calls.archive_write.c_archive_write_data_block(
                        ext, 
                        buff, 
                        size, 
                        offset)

            r = libarchive.calls.archive_write.\
                    c_archive_write_finish_entry(ext)

def file_pour(filepath, block_size=10240, *args, **kwargs):
    """Write physical files from entries."""

    def opener(archive_res):
        _logger.debug("Opening from file (file_pour): %s", filepath)
        _archive_read_open_filename(archive_res, filepath, block_size)

    return _pour(opener, *args, flags=0, **kwargs)

def memory_pour(buffer_, *args, **kwargs):
    """Yield data from entries."""

    def opener(archive_res):
        _logger.debug("Opening from (%d) bytes (memory_pour).", len(buffer_))
        _archive_read_open_memory(archive_res, buffer_)

    return _pour(opener, *args, flags=0, **kwargs)
