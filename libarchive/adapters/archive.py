import contextlib
import ctypes

import libarchive.calls.archive
import libarchive.constants.archive

def _archive_read_new():
    return libarchive.calls.archive.c_archive_read_new()

def _archive_read_support_filter_all(archive):
    return libarchive.calls.archive.c_archive_read_support_filter_all(archive)

def _archive_read_support_format_all(archive):
    return libarchive.calls.archive.c_archive_read_support_format_all(archive)

def _archive_read_support_format_7zip(archive):
    return libarchive.calls.archive.c_archive_read_support_format_7zip(archive)

def _archive_read_open_filename(archive, filepath, block_size_bytes):
    return libarchive.calls.archive.c_archive_read_open_filename(
            archive, 
            filepath, 
            block_size_bytes)

@contextlib.contextmanager
def _archive_read_next_header(archive):
    entry = ctypes.c_void_p()
    r = libarchive.calls.archive.c_archive_read_next_header(
            archive, 
            ctypes.byref(entry))

    if r == libarchive.constants.archive.ARCHIVE_OK:
        yield entry
    elif r == libarchive.constants.archive.ARCHIVE_EOF:
        yield None
    else:
        raise ValueError("Archive iteration returned error: %d" % (r))

def _archive_entry_pathname(entry):
    filepath = libarchive.calls.archive.c_archive_entry_pathname(entry)
    if filepath == None:
        raise ValueError("Could not get entry file-path.")

    return filepath

def _archive_read_data_skip(entry):
    return libarchive.calls.archive.c_archive_read_data_skip(entry)

def _archive_read_free(archive):
    return libarchive.calls.archive.c_archive_read_free(archive)

def _archive_write_set_format_7zip(archive):
    return libarchive.calls.archive.c_archive_write_set_format_7zip(archive)

_READ_FILTER_MAP = {
        'all': _archive_read_support_filter_all,
    }

_READ_FORMAT_MAP = {
        'all': _archive_read_support_format_all,
        '7z': _archive_read_support_format_7zip,
    }


class ArchiveEntry(object):
    def __init__(self, archive, entry_res):
        self.__archive = archive
        self.__entry_res = entry_res

    def __str__(self):
        return self.pathname

    @property
    def pathname(self):
        return _archive_entry_pathname(self.__entry_res)


@contextlib.contextmanager
def reader(filepath, block_size=10240, filter_name='all', format_name='all'):
    archive_res = _archive_read_new()

    try:
        _filter = _READ_FILTER_MAP[filter_name]        
        _filter(archive_res)
        
        _format = _READ_FORMAT_MAP[format_name]
        _format(archive_res)

        _archive_read_open_filename(archive_res, filepath, block_size)

        def it():
            while 1:
                with _archive_read_next_header(archive_res) as entry_res:
                    if entry_res is None:
                        break

                    yield ArchiveEntry(archive_res, entry_res)
                    _archive_read_data_skip(archive_res)

        yield it()
    finally:
        _archive_read_free(archive_res)

@contextlib.contextmanager
def pour(filepath, flags):







	a = archive_read_new();
	ext = archive_write_disk_new();
	archive_write_disk_set_options(ext, flags);
	/*
	 * Note: archive_write_disk_set_standard_lookup() is useful
	 * here, but it requires library routines that can add 500k or
	 * more to a static executable.
	 */
	archive_read_support_format_tar(a);
















class ArchiveExpand(ArchiveAccessor):
    def __init__(self, 
                 filepath, *args, **kwargs):
        self.__archive_res = None

        archive_res = _archive_write_disk_new()

        super(ArchiveReader, self).__init__(archive_res, *args, **kwargs)
        
        ext = _archive_write_disk_new(archive_res)

        self.__archive_res = archive_res
        self.__ext_res = ext

    def __write_entry(self):
static int
copy_data(struct archive *ar, struct archive *aw)
{
	int r;
	const void *buff;
	size_t size;
#if ARCHIVE_VERSION_NUMBER >= 3000000
	int64_t offset;
#else
	off_t offset;
#endif

	for (;;) {
		r = archive_read_data_block(ar, &buff, &size, &offset);
		if (r == ARCHIVE_EOF)
			return (ARCHIVE_OK);
		if (r != ARCHIVE_OK)
			return (r);
		r = archive_write_data_block(aw, buff, size, offset);
		if (r != ARCHIVE_OK) {
			warn("archive_write_data_block()",
			    archive_error_string(aw));
			return (r);
		}
	}
}

