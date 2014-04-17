import libarchive.calls.archive_write
import libarchive.exception

from libarchive.calls.archive_general import c_archive_error_string

def _archive_write_disk_new():
    archive = libarchive.calls.archive_write.c_archive_write_disk_new()
    if archive is None:
        raise ValueError("Could not create archive resource (write_disk_new)."

    return archive

def _archive_write_disk_set_options(archive, flags):
    try:
        libarchive.calls.archive_write.c_archive_write_disk_set_options(
            archive, 
            flags)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_finish_entry(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_finish_entry(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_close(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_close(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_fail(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_fail(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_free(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_free(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

# c_archive_write_data_block only applies in the reader where called directly. 
# Omitting from here.

def _archive_write_set_format_7zip(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_set_format_7zip(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)



def _archive_write_add_filter_bzip2(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_add_filter_bzip2(
            archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_add_filter_compress(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_add_filter_compress(
            archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_add_filter_gzip(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_add_filter_gzip(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_add_filter_none(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_add_filter_none(archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_set_format_ustar(archive):
    try:
        libarchive.calls.archive_write.c_archive_write_set_format_ustar(
            archive)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

def _archive_write_open_filename(archive, filepath):
    try:
        libarchive.calls.archive_write.c_archive_write_open_filename(
            archive, 
            filepath)
    except:
        message = c_archive_error_string(archive)
        raise libarchive.exception.ArchiveError(message)

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
        message = c_archive_error_string(archive)
        raise ValueError("No bytes were written. Error? [%s]" % (message))
