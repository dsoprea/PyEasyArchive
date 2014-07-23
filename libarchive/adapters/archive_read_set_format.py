import libarchive.calls.archive_read_set_format

def archive_read_set_format(archive, code):
    libarchive.calls.archive_read_set_format.c_archive_read_set_format(
        archive, 
        code)
