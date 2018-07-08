import unittest
import os
import shutil
import contextlib
import tempfile

import libarchive.adapters.archive_read
import libarchive.constants
import libarchive.test_support

_APP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# TODO(dustin): Add tests for file and memory pouring.


class TestArchiveRead(unittest.TestCase):
    def test_enumerate_from_file(self):
        with libarchive.test_support.test_archive() as filepath:
            with libarchive.adapters.archive_read.file_enumerator(filepath) as e:
                for entry in e:
                    pass

    def test_enumerate_from_memory(self):
        with libarchive.test_support.test_archive() as filepath:
            with open(filepath, 'rb') as f:
                buffer_ = f.read()
                with libarchive.adapters.archive_read.memory_enumerator(buffer_) as e:
                    for entry in e:
                        pass

    def test_read_from_file(self):
        with libarchive.test_support.test_archive() as filepath:
            with libarchive.test_support.temp_path() as output_path:
                with libarchive.adapters.archive_read.file_reader(filepath) as e:
                    for entry in e:
                        rel_filepath = entry.pathname
                        rel_path = os.path.dirname(rel_filepath)

                        if rel_path != '':
                            path = os.path.join(output_path, rel_path)

                            if os.path.exists(path) is False:
                                os.makedirs(path)

                        filepath = os.path.join(output_path, entry.pathname)

                        with open(filepath, 'wb') as f:
                            for block in entry.get_blocks():
                                f.write(block)

    def test_read_from_memory(self):
        with libarchive.test_support.test_archive() as filepath:
            with libarchive.test_support.temp_path() as output_path:
                with open(filepath, 'rb') as f:
                    buffer_ = f.read()
                    with libarchive.adapters.archive_read.memory_reader(buffer_) as e:
                        for entry in e:
                            rel_filepath = entry.pathname
                            rel_path = os.path.dirname(rel_filepath)

                            if rel_path != '':
                                path = os.path.join(output_path, rel_path)

                                if os.path.exists(path) is False:
                                    os.makedirs(path)

                            filepath = os.path.join(output_path, entry.pathname)

                            with open(filepath, 'wb') as f:
                                for block in entry.get_blocks():
                                    f.write(block)
