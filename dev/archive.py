#!/usr/bin/env python2.7

import sys
sys.path.insert(0, '..')

import libarchive

#with libarchive.reader('test.7z') as reader:
#    for e in reader:
#        print("> %s" % (e))

for entry in libarchive.pour('test.7z'):
    print("Wrote: %s" % (entry))

