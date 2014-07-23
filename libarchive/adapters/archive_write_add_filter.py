import libarchive.calls.archive_write_add_filter

def archive_write_add_filter(archive, code):
    return libarchive.calls.archive_write_add_filter.\
            c_archive_write_add_filter(archive, code)
