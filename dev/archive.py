#!/usr/bin/env python2.7

import sys
sys.path.insert(0, '..')

import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

os.environ['DYLD_LIBRARY_PATH'] = '/usr/local/Cellar/libarchive/3.1.2/lib'

import libarchive

with libarchive.reader('test.7z') as reader:
    for e in reader:
        print("> %s" % (e))

#for entry in libarchive.pour('test.7z'):
#    print("Wrote: %s" % (entry))

