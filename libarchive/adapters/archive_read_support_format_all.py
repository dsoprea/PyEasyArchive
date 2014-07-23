import libarchive.calls.archive_read_support_format_all

def archive_read_support_format_all(archive):
    return libarchive.calls.archive_read_support_format_all.\
            c_archive_read_support_format_all(archive)
