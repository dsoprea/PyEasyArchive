#!/usr/bin/env python2.7

import sys
sys.path.insert(0, '..')

import os
import logging

logger = logging.getLogger()
#logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

os.environ['DYLD_LIBRARY_PATH'] = '/Users/dustin/build/libarchive/build/libarchive'

import libarchive

#with libarchive.reader('test.7z') as reader:
#    for e in reader:
#        print("> %s" % (e))

#for entry in libarchive.pour('test.7z'):
#    print("Wrote: %s" % (entry))

for entry in libarchive.create(
                '7z', 
                ['/etc/profile'], 
                'create.7z'):
    print("Adding: %s" % (entry))
