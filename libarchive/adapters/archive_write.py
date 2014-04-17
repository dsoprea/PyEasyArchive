import libarchive.calls.archive_write

def _archive_write_disk_new():
    archive = libarchive.calls.archive_write.c_archive_write_disk_new()
    if archive is None:
        raise ValueError("Could not create archive resource (write_disk_new)."

    return archive

def _archive_write_disk_set_options(archive, flags):
    libarchive.calls.archive_write.c_archive_write_disk_set_options(
        archive, 
        flags)

def _archive_write_finish_entry(archive):
    libarchive.calls.archive_write.c_archive_write_finish_entry(archive)

def _archive_write_close(archive):
    libarchive.calls.archive_write.c_archive_write_close(archive)

def _archive_write_fail(archive):
    libarchive.calls.archive_write.c_archive_write_fail(archive)

def _archive_write_free(archive):
    libarchive.calls.archive_write.c_archive_write_free(archive)

# c_archive_write_data_block only applies in the reader where called directly. 
# Omitting from here.

def _archive_write_set_format_7zip(archive):
    libarchive.calls.archive_write.c_archive_write_set_format_7zip(archive)



def _archive_write_add_filter_bzip2(archive):
    libarchive.calls.archive_write.c_archive_write_add_filter_bzip2(archive)

def _archive_write_add_filter_compress(archive):
    libarchive.calls.archive_write.c_archive_write_add_filter_compress(archive)

def _archive_write_add_filter_gzip(archive):
    libarchive.calls.archive_write.c_archive_write_add_filter_gzip(archive)

def _archive_write_add_filter_none(archive):
    libarchive.calls.archive_write.c_archive_write_add_filter_none(archive)

def _archive_write_set_format_ustar(archive):
    libarchive.calls.archive_write.c_archive_write_set_format_ustar(archive)

def _archive_write_open_filename(archive, filepath):
    libarchive.calls.archive_write.c_archive_write_open_filename(
        archive, 
        filepath)

# archive_write_header only applies in the reader where called directly. 
# Omitting from here.

def _archive_write_data(archive, data):
    n = libarchive.calls.archive_write.c_archive_write_data(
            archive, 
# TODO(dustin): We might have to make it a c_char_p, first (maybe not, since 
#               it's immutable).
            c_void_p(data), 
            len(data))

    if n == 0:
        raise ValueError("No bytes were written.")

