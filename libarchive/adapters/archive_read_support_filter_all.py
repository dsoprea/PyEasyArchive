import libarchive.calls.archive_read_support_filter_all

def archive_read_support_filter_all(archive):
    return libarchive.calls.archive_read_support_filter_all.\
            c_archive_read_support_filter_all(archive)
