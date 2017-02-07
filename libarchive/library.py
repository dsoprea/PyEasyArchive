import logging
import os
import platform
import json
import subprocess

def _check_homebrew():
    if platform.system() == 'Darwin':
        try:
            # From homebrew on libarchive:
            # This formula is keg-only, which means it was not symlinked
            # into /usr/local.
            #
            # macOS already provides this software and installing
            # another version in parallel can cause all kinds of
            # trouble.
            #
            # so... let's see if we can't find it ourselves and set the
            # envvar
            # /Usr/local/opt/libarchive/lib/
            libarchive_info = json.loads(
                    subprocess.check_output(['brew', 'info', '--json=v1',
                        'libarchive']))
            libarchive_version = libarchive_info[0]['installed'][0]['version']
            # set the direct dylib envvar
            libarchive_path = os.path.join(subprocess.check_output([ 'brew',
                '--cellar', 'libarchive'])[:-1], libarchive_version, 'lib',
                'libarchive.dylib')
            return libarchive_path
        except Exception as e:
            return ''
    else:
        return ''

import ctypes
import ctypes.util

_logger = logging.getLogger(__name__)

_FILEPATH = os.environ.get('LA_LIBRARY_FILEPATH', _check_homebrew())
if _FILEPATH == '':
    _FILEPATH = ctypes.util.find_library('libarchive')
    if _FILEPATH is None:
        _FILEPATH = 'libarchive.so'

_logger.debug("Using library: [%s]", _FILEPATH)
libarchive = ctypes.cdll.LoadLibrary(_FILEPATH)
