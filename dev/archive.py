#!/usr/bin/env python2.7

import sys
sys.path.insert(0, '..')

import os
import logging

def configure_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to debug
    ch = logging.StreamHandler()

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

configure_logging()

os.environ['DYLD_LIBRARY_PATH'] = '/Users/dustin/build/libarchive/build/libarchive'

import libarchive

#with libarchive.file_enumerator('test.7z') as e:
#    for entry in e:
#        print(entry)

#with open('test.7z', 'rb') as f:
#    buffer_ = f.read()
#    with libarchive.memory_enumerator(buffer_) as e:
#        for entry in e:
#            print(entry)

#with libarchive.file_reader('test.7z') as e:
#    for entry in e:
#        with open('/tmp/' + str(entry), 'wb') as f:
#            for block in entry.get_blocks():
#                f.write(block)

#with open('test.7z', 'rb') as f:
#    buffer_ = f.read()
#    with libarchive.memory_reader(buffer_) as e:
#        for entry in e:
#            with open('/tmp/' + str(entry), 'wb') as f:
#                for block in entry.get_blocks():
#                    f.write(block)

for entry in libarchive.create_file(
                'create.7z',
                '7z', 
                ['/etc/profile']):
    print("Adding: %s" % (entry))

#for entry in libarchive.create_memory(
#                '7z', 
#                []):
#    print("Adding: %s" % (entry))

#libarchive.create_file('create.7z', '7z', ['/etc/profile'])
#libarchive.create_memory('7z', [])
