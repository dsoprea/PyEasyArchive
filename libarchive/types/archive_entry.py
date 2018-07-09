import collections

import libarchive.constants.archive_entry

ENTRY_FILETYPE = \
    collections.namedtuple('ENTRY_FILETYPE', [
        'IFREG',
        'IFLNK',
        'IFSOCK',
        'IFCHR',
        'IFBLK',
        'IFDIR',
        'IFIFO',
    ])

def ef_to_int(ef):
    n = 0
    for name, value in libarchive.constants.archive_entry.FILETYPES.items():
        if getattr(ef, name) is True:
            n |= value

    return n

def int_to_ef(n):
    """This is here for testing support but, in practice, this isn't very
    useful as many of the flags are just combinations of other flags. The
    relationships are defined by the OS in ways that aren't semantically
    intuitive to this project.
    """

    flags = {}
    for name, value in libarchive.constants.archive_entry.FILETYPES.items():
        flags[name] = (n & value) > 0

    return ENTRY_FILETYPE(**flags)
