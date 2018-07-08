import unittest
import os
import shutil
import contextlib
import tempfile

import libarchive.adapters.archive_write
import libarchive.adapters.archive_read
import libarchive.constants
import libarchive.test_support

_APP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')

# TODO(dustin): Add tests for file and memory pouring.


class TestArchiveWrite(unittest.TestCase):
    def test_create_file(self):
        with libarchive.test_support.chdir(_APP_PATH):
            output_path = tempfile.mkdtemp()

            output_filename = 'archive.7z'
            output_filepath = os.path.join(output_path, output_filename)

            try:
                files = [
                    'libarchive/resources/README.rst',
                    'libarchive/resources/requirements.txt',
                ]

                libarchive.adapters.archive_write.create_file(
                    output_filepath,
                    libarchive.constants.ARCHIVE_FORMAT_7ZIP,
                    files)

                assert \
                    os.path.exists(output_filepath) is True, \
                    "Test archive was not created correctly."

                with libarchive.adapters.archive_read.file_enumerator(output_filepath) as e:
                    actual = [entry.pathname for entry in e]
            finally:
                try:
                    shutil.rmtree(output_path)
                except:
                    pass

            expected = [
                'libarchive/resources/README.rst',
                'libarchive/resources/requirements.txt',
            ]

            self.assertEquals(actual, expected)
