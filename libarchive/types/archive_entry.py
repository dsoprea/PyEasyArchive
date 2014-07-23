import collections

ENTRY_FILETYPE = collections.namedtuple('EntryFileType', [
    'IFREG',
    'IFLNK',
    'IFSOCK',
    'IFCHR',
    'IFBLK',
    'IFDIR',
    'IFIFO'])
