import os
import os.path
import shutil

import libarchive.public
import libarchive.constants

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
    for entry in libarchive.public.create_file(
                    _TEST_CREATE_ARCHIVE,
                    libarchive.constants.ARCHIVE_FORMAT_7ZIP, 
                    ['/etc/hosts']):
        pass

test_create_to_file_from_file.setUp = _setup
test_create_to_file_from_file.tearDown = _teardown

# TODO(dustin): This segfaults during the test, for some reason.
#def test_create_to_memory_from_file():
#    def writer(buffer_, length):
#        return length
#
#    with open(_TEST_CREATE_ARCHIVE, 'wb') as f:
#        for entry in libarchive.public.create_generic(
#                        writer,
#                        format_code=libarchive.constants.ARCHIVE_FORMAT_7ZIP, 
#                        files=['/etc/hosts']):
#            pass
#
#test_create_to_memory_from_file.setUp = _setup
#test_create_to_memory_from_file.tearDown = _teardown

