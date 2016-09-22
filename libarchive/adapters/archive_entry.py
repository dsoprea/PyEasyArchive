import ctypes
import datetime

import libarchive.constants.archive_entry
import libarchive.types.archive_entry
import libarchive.calls.archive_entry

def _archive_entry_pathname(entry):
    filepath = libarchive.calls.archive_entry.c_archive_entry_pathname(entry)
    if filepath is None:
        raise ValueError("Could not get entry file-path.")

    return filepath

def archive_entry_new():
    entry = libarchive.calls.archive_entry.c_archive_entry_new()
    if entry is None:
        raise ValueError("Could not get new entry.")

    return entry

def _archive_entry_sourcepath(entry):
    return libarchive.calls.archive_entry.c_archive_entry_sourcepath(entry)

def _archive_entry_free(entry):
    libarchive.calls.archive_entry.c_archive_entry_free(entry)

def _archive_entry_size(entry):
    return libarchive.calls.archive_entry.c_archive_entry_size(entry)

def _archive_entry_set_pathname(entry, name):
    libarchive.calls.archive_entry.c_archive_entry_set_pathname(
        entry, 
        ctypes.c_char_p(name))

def _archive_entry_filetype(entry):
    return libarchive.calls.archive_entry.c_archive_entry_filetype(entry)

def _archive_entry_mtime(entry):
    return libarchive.calls.archive_entry.c_archive_entry_mtime(entry)

def _archive_entry_perm(entry):
    return libarchive.calls.archive_entry.c_archive_entry_perm(entry)


class ArchiveEntry(object):
    def __init__(self, reader_res, entry_res):
        self.__reader_res = reader_res
        self.__entry_res = entry_res
        self.__is_consumed = False

# TODO(dustin): Not necessary, at least during the read.
#    def __del__(self):
#        _archive_entry_free(self.__entry_res)

    def __str__(self):
        return self.pathname

    def __repr__(self):
        return ('[%s] SIZE=(%d)' % (self.pathname, self.size))

    @property
    def reader_res(self):
        return self.__reader_res

    @property
    def entry_res(self):
        return self.__entry_res

    def read_block(self):
        for block in _read_by_block(self.reader_res):
            yield block

        self.__is_consumed = True

    @property
    def is_consumed(self):
        return self.__is_consumed

    @property
    def pathname(self):
        return _archive_entry_pathname(self.__entry_res)

    @pathname.setter
    def pathname(self, value):
        _archive_entry_set_pathname(self.__entry_res, value)

    @property
    def sourcepath(self):
        return _archive_entry_sourcepath(self.__entry_res)

    @property
    def size(self):
        return _archive_entry_size(self.__entry_res)

    @property
    def filetype(self):
        filetype = _archive_entry_filetype(self.__entry_res)
        flags = dict([(k, v == filetype) 
                      for (k, v) 
                      in libarchive.constants.archive_entry.FILETYPES.items()])

        return libarchive.types.archive_entry.ENTRY_FILETYPE(**flags)

    @property
    def mtime(self):
        return datetime.datetime.fromtimestamp(
                                    _archive_entry_mtime(self.__entry_res))

    @property
    def perm(self):
        return _archive_entry_perm(self.__entry_res)
