import logging
import os

import ctypes
import ctypes.util

_LOGGER = logging.getLogger(__name__)

_LIBRARY_NAME = 'libarchive'
_LIBRARY_FILENAME = 'libarchive.so'

def find_and_load_library():
    search_filepaths = []

    # Search for the library using our own environment variable.

    filepath = os.environ.get('LA_LIBRARY_FILEPATH', '')
    if filepath != '':
        search_filepaths.append(filepath)

    # Search for the library using the well-defined system library search-path.

    _SEARCH_PATH = os.environ.get('LD_LIBRARY_PATH', '')
    if _SEARCH_PATH != '':
        for path in _SEARCH_PATH.split(":"):
            filepath = os.path.join(path, _LIBRARY_FILENAME)
            search_filepaths.append(filepath)

    # Search for our library using whatever search-path ctypes uses (not the same 
    # as `LD_LIBRARY_PATH`).

    filepath = ctypes.util.find_library(_LIBRARY_NAME)
    if filepath is not None:
        search_filepaths.append(filepath)

    # Load the first one available.

    found_filepath = None
    for filepath in search_filepaths:
        if os.path.exists(filepath) is True:
            return filepath

    # Fallback on the naively trying to load the filename.

    _LOGGER.debug("Using default library file-path: [%s]", _LIBRARY_FILENAME)
    return _LIBRARY_FILENAME

_FILEPATH = find_and_load_library()

_LOGGER.debug("Using library file-path: [%s]", _FILEPATH)
libarchive = ctypes.cdll.LoadLibrary(_FILEPATH)
