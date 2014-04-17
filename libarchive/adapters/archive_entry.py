import libarchive.calls.archive_entry

def _archive_entry_pathname(entry):
    filepath = libarchive.calls.archive_entry.c_archive_entry_pathname(entry)
    if filepath is None:
        raise ValueError("Could not get entry file-path.")

    return filepath

# TODO(dustin): Still unimplemented. This should probably be called from a
#               reading or writing context when needed, or we won't be able to 
#               create the entry-object, below, while equipping it with that 
#               archive resource (like we sometimes depend on).
def archive_entry_new():
    entry = libarchive.calls.archive_entry.c_archive_entry_new()
    if entry is None:
        raise ValueError("Could not get new entry.")

    return entry

def _archive_entry_sourcepath(entry):
    return libarchive.calls.archive_entry.c_archive_entry_sourcepath(entry)

def _archive_entry_free(entry):
    libarchive.calls.archive_entry.c_archive_entry_free(entry)


class ArchiveEntry(object):
    def __init__(self, reader_res, entry_res):
        self.__reader_res = reader_res
        self.__entry_res = entry_res

    def __del__(self):
        _archive_entry_free(self.__entry_res)

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

    @property
    def sourcepath(self):
        return _archive_entry_sourcepath(self.__entry_res)

