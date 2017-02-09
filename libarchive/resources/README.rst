------------
Introduction
------------

A ctypes-based adapter to libarchive. The source-code is written to be clear 
and intuitive.

Even 7-Zip is supported for both reading and writing.

I could definitely use some help, if any is available. Completeness will 
require a bit more work (see *libarchive*'s archive.h and archive_entry.h).


------------
Installation
------------

PyPI::

    $ sudo pip install libarchive


-----
Notes
-----

- The Ubuntu `libarchive` package maintainer only provides a "libarchive.so" symlink in the dev package so you'll have to install the `libarchive-dev` package.

  For example::

    apt-get install libarchive-dev
    
- Encryption is not currently supported since it's not supported in the underlying library (*libarchive*). Note `this inquiry <https://github.com/libarchive/libarchive/issues/579>`_ and the `wishlist item <https://github.com/libarchive/libarchive/wiki/WishList#encrypted-backup-support>`_.

- OS X has a system version of `libarchive` that is very old. As a result, many users have encountered issues importing an alternate one. Specifically, often they install a different one via Brew but this will not be [sym]linked into the system like other packages. This is a precaution taken by Brew to prevent undefined behavior in the parts of OS X that depend on the factory version. In order to work around this, you should set `LD_LIBRARY_PATH` (or prepend if `LD_LIBRARY_PATH` is already defined) with the path of the location of the library version you want to use. You'll want to set this from your user-profile script (unless your environment can not support this and you need to prepend something like "LD_LIBRARY_PATH=/some/path" to the front of the command-line or set it via `os.environ` above where you import this package). A `tool <tools/brew_find_libarchive>`_ has been provided that will print the path of the first version of `libarchive` installed via Brew. Just copy-and-paste it. Thanks to @SkyLeach for discussing the issue and treatments.


---------
Task List
---------

=====  =================================================
Done   Task
=====  =================================================
  X    Read entries from physical file
  X    Read entries from archive hosted in memory buffer
  X    Write physical files from archive
  X    Load memory buffer from archive
  X    Populate physical archive from physical files
  X    Populate archive hosted in memory buffer
  _    Populate archive entries from memory buffers
  _    Fill-out the entry object's information/accessors
=====  =================================================


--------
Examples
--------

To extract to the current directory from a physical file (and print each 
relative filepath)::

    import libarchive.public

    for entry in libarchive.public.file_pour('/tmp/test.zip'):
        print(entry)

To extract to the current directory from memory::

    import libarchive.public

    with open('/tmp/test.zip', 'rb') as f:
        for entry in libarchive.public.memory_pour(f.read()):
            print(entry)

To read files from a physical archive::

    import libarchive.public

    with libarchive.public.file_reader('test.7z') as e:
        for entry in e:
            with open('/tmp/' + str(entry), 'wb') as f:
                for block in entry.get_blocks():
                    f.write(block)

To read files from memory::

    import libarchive.public

    with open('test.7z', 'rb') as f:
        buffer_ = f.read()
        with libarchive.public.memory_reader(buffer_) as e:
            for entry in e:
                with open('/tmp/' + str(entry), 'wb') as f:
                    for block in entry.get_blocks():
                        f.write(block)

To specify a format and/or filter for reads (rather than detecting it)::

    import libarchive.public
    import libarchive.constants

    with open('test.7z', 'rb') as f:
        buffer_ = f.read()
        with libarchive.public.memory_reader(
                buffer_,
                format_code=libarchive.constants.ARCHIVE_FORMAT_TAR_USTAR, 
                filter_code=libarchive.constants.ARCHIVE_FILTER_GZIP
            ) as e:
            for entry in e:
                with open('/tmp/' + str(entry), 'wb') as f:
                    for block in entry.get_blocks():
                        f.write(block)

To read the "filetype" flag for each entry::

    import libarchive.public

    with open('test.7z', 'rb') as f:
        buffer_ = f.read()
        with libarchive.public.memory_reader(f.read()) as e:
            for entry in e:
                print(entry.filetype)

The output of this is::

    EntryFileType(IFREG=True, IFLNK=True, IFSOCK=True, IFCHR=False, IFBLK=False, IFDIR=False, IFIFO=False)
    EntryFileType(IFREG=True, IFLNK=True, IFSOCK=True, IFCHR=False, IFBLK=False, IFDIR=False, IFIFO=False)
    EntryFileType(IFREG=True, IFLNK=True, IFSOCK=True, IFCHR=False, IFBLK=False, IFDIR=False, IFIFO=False)

To create a physical archive from physical files::

    import libarchive.public
    import libarchive.constants

    for entry in libarchive.public.create_file(
                    'create.7z',
                    libarchive.constants.ARCHIVE_FORMAT_7ZIP, 
                    ['/etc/profile']):
        print(entry)

To create an archive in memory from physical files::

    import libarchive.public
    import libarchive.constants

    with open('/tmp/new.7z', 'wb') as f:
        def writer(buffer_, length):
            f.write(buffer_)
            return length

        for entry in libarchive.public.create_generic(
                        writer,
                        format_name=libarchive.constants.ARCHIVE_FORMAT_7ZIP, 
                        files=['/etc/profile']):
            print(entry)


-------
Testing
-------

*libarchive* uses `nose <https://nose.readthedocs.org>`_ for testing::

    tests$ ./run.py
