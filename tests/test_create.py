import os
import os.path

import libarchive

_TEST_CREATE_ARCHIVE = 'resources/create.7z'

def test_create_to_file_from_file():
    for entry in libarchive.create(
                    '7z', 
                    ['/etc/profile'], 
                    _TEST_CREATE_ARCHIVE):
        pass

def _setup():
    if os.path.exists(_TEST_CREATE_ARCHIVE) is True:
        os.unlink(_TEST_CREATE_ARCHIVE)

def _teardown():
    os.unlink(_TEST_CREATE_ARCHIVE)

test_create_to_file_from_file.setUp = _setup
test_create_to_file_from_file.tearDown = _teardown
