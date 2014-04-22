#!/usr/bin/env python2.7

import sys
sys.path.insert(0, '..')

import os
import os.path
import nose

mac_library_path = '/Users/dustin/build/libarchive/build/libarchive'
if os.path.exists(mac_library_path) is True:
    os.environ['DYLD_LIBRARY_PATH'] = mac_library_path

nose.run()
