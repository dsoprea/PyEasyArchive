import os
import os.path
import shutil

import libarchive.public
import libarchive.constants

_EXPAND_PATH = os.path.join('/tmp', 'libarchive_expand')
_TEST_READ_ARCHIVE = os.path.join(_EXPAND_PATH, 'read.7z')

# TODO(dustin): Add tests for file and memory pouring.

def _setup():
    if os.path.exists(_EXPAND_PATH) is True:
        shutil.rmtree(_EXPAND_PATH)

    os.mkdir(_EXPAND_PATH)

    for entry in libarchive.public.create_file(
                    _TEST_READ_ARCHIVE,
                    libarchive.constants.ARCHIVE_FORMAT_7ZIP, 
                    ['/etc/hosts',
                     'resources/man.conf']):
        pass

def _teardown():
    if os.path.exists(_EXPAND_PATH) is True:
        shutil.rmtree(_EXPAND_PATH)

def test_enumerate_from_file():
    with libarchive.public.file_enumerator(_TEST_READ_ARCHIVE) as e:
        for entry in e:
            pass

test_enumerate_from_file.setUp = _setup
test_enumerate_from_file.tearDown = _teardown

def test_enumerate_from_memory():
    with open(_TEST_READ_ARCHIVE, 'rb') as f:
        buffer_ = f.read()
        with libarchive.public.memory_enumerator(buffer_) as e:
            for entry in e:
                pass

test_enumerate_from_memory.setUp = _setup
test_enumerate_from_memory.tearDown = _teardown

def _tree_writer(e):
    for entry in e:
        rel_filepath = entry.pathname
        rel_path = os.path.dirname(rel_filepath)

        if rel_path != '':
            path = os.path.join(_EXPAND_PATH, rel_path)

            if os.path.exists(path) is False:
                os.makedirs(path)

        filepath = os.path.join(_EXPAND_PATH, entry.pathname)
        
        with open(filepath, 'wb') as f:
            for block in entry.get_blocks():
                f.write(block)

def test_read_from_file():
    with libarchive.public.file_reader(_TEST_READ_ARCHIVE) as e:
        _tree_writer(e)

test_read_from_file.setUp = _setup
test_read_from_file.tearDown = _teardown

def test_read_from_memory():
    with open(_TEST_READ_ARCHIVE, 'rb') as f:
        buffer_ = f.read()
        with libarchive.public.memory_reader(buffer_) as e:
            _tree_writer(e)

test_read_from_memory.setUp = _setup
test_read_from_memory.tearDown = _teardown
