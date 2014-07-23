import libarchive.calls.archive_read_append_filter

def archive_read_append_filter(archive, code):
    return libarchive.calls.archive_read_append_filter.\
            c_archive_read_append_filter(archive, code)
