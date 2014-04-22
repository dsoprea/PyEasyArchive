import os
import os.path
import shutil

import libarchive

_TEMP_PATH = os.path.join('/tmp', 'libarchive_expand')
_TEST_CREATE_ARCHIVE = os.path.join(_TEMP_PATH, 'create.7z')

def _setup():
    if os.path.exists(_TEMP_PATH) is True:
        shutil.rmtree(_TEMP_PATH)

    os.mkdir(_TEMP_PATH)

def _teardown():
    if os.path.exists(_TEMP_PATH) is True:
        shutil.rmtree(_TEMP_PATH)

def test_create_to_file_from_file():
    for entry in libarchive.create_file(
                    _TEST_CREATE_ARCHIVE,
                    '7z', 
                    ['/etc/hosts']):
        pass

test_create_to_file_from_file.setUp = _setup
test_create_to_file_from_file.tearDown = _teardown
