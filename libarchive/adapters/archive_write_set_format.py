import libarchive.calls.archive_write_set_format

def archive_write_set_format(archive, code):
    libarchive.calls.archive_write_set_format.c_archive_write_set_format(
        archive, 
        code)
