#!/usr/bin/env python2.7

import sys
sys.path.insert(0, '..')

import libarchive

a = libarchive.Archive('test.7z')
for e in a.read():
    print("> %s" % (e))

