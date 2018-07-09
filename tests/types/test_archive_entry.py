import unittest

import libarchive.constants.archive_entry
import libarchive.types.archive_entry


class TestArchiveEntry(unittest.TestCase):
    def test_cycle(self):
        # Four of the flags represent individual bits and the other four flags
        # represent different combinations of the same bits.
        ef = libarchive.types.archive_entry.ENTRY_FILETYPE(
                IFREG=True,
                IFLNK=False,
                IFSOCK=False,
                IFCHR=True,
                IFBLK=False,
                IFDIR=True,
                IFIFO=True)

        n = libarchive.types.archive_entry.ef_to_int(ef)

        expected_n = \
            libarchive.constants.archive_entry.AE_IFREG | \
            libarchive.constants.archive_entry.AE_IFCHR | \
            libarchive.constants.archive_entry.AE_IFDIR | \
            libarchive.constants.archive_entry.AE_IFIFO | \
            libarchive.constants.archive_entry.AE_IFSOCK | \
            libarchive.constants.archive_entry.AE_IFLNK | \
            libarchive.constants.archive_entry.AE_IFBLK | \
            libarchive.constants.archive_entry.AE_IFMT

        self.assertEquals(n, expected_n)

        recovered = libarchive.types.archive_entry.int_to_ef(n)

        expected_ef = \
            libarchive.types.archive_entry.ENTRY_FILETYPE(
                IFREG=True,
                IFLNK=True,
                IFSOCK=True,
                IFCHR=True,
                IFBLK=True,
                IFDIR=True,
                IFIFO=True)

        self.assertEquals(recovered, expected_ef)
