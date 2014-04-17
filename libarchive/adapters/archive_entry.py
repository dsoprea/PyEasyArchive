import libarchive.calls.archive_entry

def _archive_entry_pathname(entry):
    filepath = libarchive.calls.archive_entry.c_archive_entry_pathname(entry)
    if filepath == None:
        raise ValueError("Could not get entry file-path.")

    return filepath


class ArchiveEntry(object):
    def __init__(self, reader_res, entry_res):
        self.__reader_res = reader_res
        self.__entry_res = entry_res

    def __str__(self):
        return self.pathname

    @property
    def reader_res(self):
        return self.__reader_res

    @property
    def entry_res(self):
        return self.__entry_res

    @property
    def pathname(self):
        return _archive_entry_pathname(self.__entry_res)

