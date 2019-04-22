import ctypes
import datetime

import libarchive.constants.archive_entry
import libarchive.types.archive_entry
import libarchive.calls.archive_entry

def _archive_entry_pathname(entry):
    filepath = libarchive.calls.archive_entry.c_archive_entry_pathname(entry)
    if filepath is None:
        raise ValueError("Could not get entry file-path.")

    return filepath.decode('utf-8')

def archive_entry_new():
    entry = libarchive.calls.archive_entry.c_archive_entry_new()
    if entry is None:
        raise ValueError("Could not get new entry.")

    return entry

def _archive_entry_sourcepath(entry):
    raw = libarchive.calls.archive_entry.c_archive_entry_sourcepath(entry)
    return raw.decode('utf-8')

def _archive_entry_free(entry):
    libarchive.calls.archive_entry.c_archive_entry_free(entry)

def _archive_entry_size(entry):
    return libarchive.calls.archive_entry.c_archive_entry_size(entry)

def _archive_entry_set_size(entry, size):
    return libarchive.calls.archive_entry.c_archive_entry_set_size(entry, size)

def _archive_entry_set_pathname(entry, name):
    name = name.encode('utf-8')

    libarchive.calls.archive_entry.c_archive_entry_set_pathname(
        entry,
        ctypes.c_char_p(name))

def _archive_entry_filetype(entry):
    return libarchive.calls.archive_entry.c_archive_entry_filetype(entry)

def _archive_entry_set_filetype(entry, filetype):
    return libarchive.calls.archive_entry.c_archive_entry_set_filetype(entry, filetype)

def _archive_entry_mtime(entry):
    return libarchive.calls.archive_entry.c_archive_entry_mtime(entry)

def _archive_entry_perm(entry):
    return libarchive.calls.archive_entry.c_archive_entry_perm(entry)

def _archive_entry_symlink(entry):
    encoded = libarchive.calls.archive_entry.c_archive_entry_symlink(entry)
    decoded = encoded.decode('utf-8')

    return decoded

def _archive_entry_set_symlink(entry, target_filepath):
    encoded = target_filepath.encode('utf-8')
    return libarchive.calls.archive_entry.c_archive_entry_set_symlink(entry, encoded)


class ArchiveEntry(object):
    def __init__(self, reader_res, entry_res):
        self.__reader_res = reader_res
        self.__entry_res = entry_res
        self.__is_consumed = False

# TODO(dustin): Not necessary, at least during the read.
#    def __del__(self):
#        _archive_entry_free(self.__entry_res)

    def __str__(self):
        suffix_parts = []
        if self.filetype.IFLNK is True:
            suffix_parts.append('TARGET-PATH=[{}]'.format(self.symlink_targetpath))

        if suffix_parts:
            suffix = ' ' + ' '.join(suffix_parts)
        else:
            suffix = ''

        return \
            'ArchiveEntry<NAME=[{}] SIZE=({}){}>'.format(
            self.pathname, self.size, suffix)

    __repr__ = __str__

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
        """Path in the archive."""

        return _archive_entry_pathname(self.__entry_res)

    @pathname.setter
    def pathname(self, value):
        """Path in the archive."""

        _archive_entry_set_pathname(self.__entry_res, value)

    @property
    def sourcepath(self):
        """Path on the disk."""

        return _archive_entry_sourcepath(self.__entry_res)

    @property
    def size(self):
        return _archive_entry_size(self.__entry_res)

    @size.setter
    def size(self, size):
        _archive_entry_set_size(self.__entry_res, size)

    @property
    def filetype(self):
        filetype = _archive_entry_filetype(self.__entry_res)
        flags = dict([(k, v == filetype)
                      for (k, v)
                      in libarchive.constants.archive_entry.FILETYPES.items()])

        return libarchive.types.archive_entry.ENTRY_FILETYPE(**flags)

    @filetype.setter
    def filetype(self, filetype):
        filetype_int = libarchive.types.archive_entry.ef_to_int(filetype)
        _archive_entry_set_filetype(self.__entry_res, filetype_int)

    @property
    def mtime(self):
        return datetime.datetime.fromtimestamp(
                                    _archive_entry_mtime(self.__entry_res))

    @property
    def perm(self):
        return _archive_entry_perm(self.__entry_res)

    @property
    def symlink_targetpath(self):
        return _archive_entry_symlink(self.__entry_res)

    @symlink_targetpath.setter
    def symlink_targetpath(self, target_filepath):
        return _archive_entry_set_symlink(self.__entry_res, target_filepath)
