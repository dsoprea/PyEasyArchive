import contextlib
import ctypes

import libarchive.calls.archive
import libarchive.constants.archive

def _archive_read_new():
    return libarchive.calls.archive.c_archive_read_new()

def _archive_read_support_filter_all(archive):
    return libarchive.calls.archive.c_archive_read_support_filter_all(archive)

def _archive_read_support_format_all(archive):
    return libarchive.calls.archive.c_archive_read_support_format_all(archive)

def _archive_read_open_filename(archive, filepath, block_size_bytes):
    return libarchive.calls.archive.c_archive_read_open_filename(
            archive, 
            filepath, 
            block_size_bytes)

@contextlib.contextmanager
def _archive_read_next_header(archive):
    entry = ctypes.c_void_p()
    r = libarchive.calls.archive.c_archive_read_next_header(
            archive, 
            ctypes.byref(entry))

    if r == libarchive.constants.archive.ARCHIVE_OK:
        yield entry
    elif r == libarchive.constants.archive.ARCHIVE_EOF:
        yield None
    else:
        raise ValueError("Archive iteration returned error: %d" % (r))

def _archive_entry_pathname(entry):
    filepath = libarchive.calls.archive.c_archive_entry_pathname(entry)
    if filepath == None:
        raise ValueError("Could not get entry file-path.")

    return filepath

def _archive_read_data_skip(entry):
    return libarchive.calls.archive.c_archive_read_data_skip(entry)

def _archive_read_free(archive):
    return libarchive.calls.archive.c_archive_read_free(archive)


class ArchiveEntry(object):
    def __init__(self, archive, entry_res):
        self.__archive = archive
        self.__entry_res = entry_res

    def __str__(self):
        return self.pathname

    @property
    def pathname(self):
        return _archive_entry_pathname(self.__entry_res)


class Archive(object):
    def __init__(self, filepath, block_size=10240):
        self.__archive_res = None
        
        archive_res = _archive_read_new()
        _archive_read_support_filter_all(archive_res)
        _archive_read_support_format_all(archive_res)
        _archive_read_open_filename(archive_res, filepath, block_size)

        self.__archive_res = archive_res

    def read(self):
        """Return a generator to read through the archive entries."""

        while 1:
            with _archive_read_next_header(self.__archive_res) as entry:
                if entry is None:
                    break

                yield ArchiveEntry(self, entry)
                _archive_read_data_skip(self.__archive_res)

    def __del__(self):
        if self.__archive_res is not None:
            _archive_read_free(self.__archive_res)

