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
            temp_path = tempfile.mkdtemp()

            output_filename = 'archive.7z'
            output_filepath = os.path.join(temp_path, output_filename)

            try:
                files = [
                    'libarchive/resources/README.rst',
                    'libarchive/resources/requirements.txt',
                ]

                libarchive.adapters.archive_write.create_file(
                    output_filepath,
                    libarchive.constants.ARCHIVE_FORMAT_TAR,
                    files,
                    filter_code=libarchive.constants.ARCHIVE_FILTER_BZIP2)

                assert \
                    os.path.exists(output_filepath) is True, \
                    "Test archive was not created correctly."

                with libarchive.adapters.archive_read.file_enumerator(output_filepath) as e:
                    actual = [entry.pathname for entry in e]
            finally:
                try:
                    shutil.rmtree(temp_path)
                except:
                    pass

            expected = [
                'libarchive/resources/README.rst',
                'libarchive/resources/requirements.txt',
            ]

            self.assertEquals(actual, expected)

    def test_create_file__unicode(self):
        with libarchive.test_support.chdir(_APP_PATH):
            temp_path = tempfile.mkdtemp()

            output_filename = 'archive.7z'
            output_filepath = os.path.join(temp_path, output_filename)

            # Also, write a source file with a unicode name that we can add to
            # test internation support.
            unicode_test_filepath = \
                os.path.join(
                    temp_path,
                    "\u0905\u0906\u0907\u0536\u0537\u0538\u0539\u053a\u053b\uac12\uac13\uac14\uac15\uac16")

            with open(unicode_test_filepath, 'w') as f:
                f.write("test data \uf91f\uf920\uf921\uf922\uf923\uf924\uf925")

            try:
                files = [
                    'libarchive/resources/README.rst',
                    'libarchive/resources/requirements.txt',
                    unicode_test_filepath,
                ]

                libarchive.adapters.archive_write.create_file(
                    output_filepath,
                    libarchive.constants.ARCHIVE_FORMAT_TAR,
                    files,
                    filter_code=libarchive.constants.ARCHIVE_FILTER_BZIP2)

                assert \
                    os.path.exists(output_filepath) is True, \
                    "Test archive was not created correctly."

                with libarchive.adapters.archive_read.file_enumerator(output_filepath) as e:
                    actual = [entry.pathname for entry in e]
            finally:
                try:
                    shutil.rmtree(temp_path)
                except:
                    pass

            expected = [
                'libarchive/resources/README.rst',
                'libarchive/resources/requirements.txt',
                unicode_test_filepath.lstrip(os.sep),
            ]

            self.assertEquals(actual, expected)
