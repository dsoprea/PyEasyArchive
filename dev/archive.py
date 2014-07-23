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
import libarchive.constants.archive

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

#for entry in libarchive.create_file(
#                'create.7z',
#                '7z', 
#                ['/etc/profile']):
#    print("Adding: %s" % (entry))

#with open('/tmp/new.7z', 'wb') as f:
#    def writer(buffer_, length):
#        f.write(buffer_)
#        return length
#
#    def opener():
#        print("Opening.")
#    
#    def closer():
#        print("Closing.")
#
#    for entry in libarchive.create_generic(
#                    writer,
#                    open_cb=opener,
#                    close_cb=closer,
#                    format_name='7z', 
#                    files=['/etc/profile']):
#        print("Adding: %s" % (entry))

#libarchive.create_file('create.7z', '7z', ['/etc/profile'])
#libarchive.create_memory('7z', [])

def expand_deb_memory():
    with open('/Users/dustin/Downloads/op-adam-665.deb', 'rb') as f:
        buffer_ = f.read()
        with libarchive.memory_reader(
                buffer_,
    #            format_code=libarchive.constants.archive.ARCHIVE_FORMAT_ZIP
            ) as e:
            for entry in e:
                path = '/tmp/deb/' + str(entry)

                if not entry.filetype.IFDIR:
                    with open(path, 'wb') as f:
                        written = 0
                        for block in entry.get_blocks():
                            f.write(block)
                            written += len(block)

                        assert written == entry.size
                elif os.path.exists(path) is False:
                    os.mkdir(path)

    with open('/tmp/deb/data.tar.gz', 'rb') as f:
        buffer_ = f.read()
        with libarchive.memory_reader(
                buffer_,
                format_code=libarchive.constants.archive.ARCHIVE_FORMAT_TAR_USTAR, 
                filter_code=libarchive.constants.archive.ARCHIVE_FILTER_GZIP
            ) as e:
            for entry in e:
                path = '/tmp/data/' + str(entry)

                if not entry.filetype.IFDIR:
                    with open(path, 'wb') as f:
                        written = 0
                        for block in entry.get_blocks():
                            f.write(block)
                            written += len(block)

                        assert written == entry.size
                elif os.path.exists(path) is False:
                    os.mkdir(path)

def expand_deb_file():
    with libarchive.file_reader('/Users/dustin/Downloads/op-adam-665.deb') as e:
        for entry in e:
            with open('/tmp/deb/' + str(entry), 'wb') as f:
                for block in entry.get_blocks():
                    f.write(block)

    with libarchive.file_reader('/tmp/deb/data.tar.gz') as e:
        for entry in e:
            path = '/tmp/data/' + str(entry)

            if not entry.filetype.IFDIR:
                with open(path, 'wb') as f:
                    written = 0
                    for block in entry.get_blocks():
                        f.write(block)
                        written += len(block)

                    assert written == entry.size
            elif os.path.exists(path) is False:
                os.mkdir(path)

def pour_deb_file():
    os.chdir('/tmp/deb')
    for e in libarchive.file_pour('/Users/dustin/Downloads/op-adam-665.deb'):
        print(e)

    print('')

    os.chdir('/tmp/data')
    for e in libarchive.file_pour('/tmp/deb/data.tar.gz'):
        print(e)

def pour_deb_memory():
    os.chdir('/tmp/deb')
    with open('/Users/dustin/Downloads/op-adam-665.deb', 'rb') as f:
        for e in libarchive.memory_pour(f.read()):
            print(e.filetype)

#    print('')
#
#    os.chdir('/tmp/data')
#    with open('/tmp/deb/data.tar.gz', 'rb') as f:
#        for e in libarchive.memory_pour(f.read()):
#            print(e)

pour_deb_memory()
