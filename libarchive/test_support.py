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
                'README.rst',
                'libarchive/resources/README.rst',
                'libarchive/resources/requirements.txt',
                unicode_test_filepath,
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
                shutil.rmtree(temp_path)
            except:
                pass
