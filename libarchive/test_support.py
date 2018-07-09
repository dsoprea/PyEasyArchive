import os
import shutil
import tempfile
import contextlib

import libarchive.public

_APP_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

@contextlib.contextmanager
def temp_path():
    path = tempfile.mkdtemp()
    original_path = os.getcwd()

    os.chdir(path)

    try:
        yield path
    finally:
        os.chdir(original_path)

        try:
            shutil.rmtree(path)
        except:
            pass

@contextlib.contextmanager
def chdir(path):
    original_path = os.getcwd()

    os.chdir(path)

    try:
        yield path
    finally:
        os.chdir(original_path)

@contextlib.contextmanager
def test_archive():
    with chdir(_APP_PATH):
        output_path = tempfile.mkdtemp()

        output_filename = 'archive.7z'
        output_filepath = os.path.join(output_path, output_filename)

        try:
            files = [
                'README.rst',
                'libarchive/resources/README.rst',
                'libarchive/resources/requirements.txt',
            ]

            libarchive.public.create_file(
                output_filepath,
                libarchive.constants.ARCHIVE_FORMAT_7ZIP,
                files)

            assert \
                os.path.exists(output_filepath) is True, \
                "Test archive was not created correctly."

            yield output_filepath
        finally:
            try:
                shutil.rmtree(output_path)
            except:
                pass
