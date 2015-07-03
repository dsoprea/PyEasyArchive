**To eliminate some problems with installation, the public API has been moved from the `libarchive` package to `libarchive.public`, and will be reflected in the next release. This is backwards-incompatible, but would otherwise prevent the install due to broken dependencies during install.**

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

- The Ubuntu *libarchive* package maintainer refuses to place a "libarchive.so" symlink, so you'll have to place this yourself. Depending on your Ubuntu, this can be libarchive.so.12, libarchive.so.13, or libarchive.so.14 .

  For example::

    /usr/lib/x86_64-linux-gnu$ sudo ln -s libarchive.so.12 libarchive.so

- Encryption is not currently supported since it's not supported in the underlying library (*libarchive*). Note `this inquiry <https://github.com/libarchive/libarchive/issues/579>`_ and the `wishlist item <https://github.com/libarchive/libarchive/wiki/WishList#encrypted-backup-support>`_.


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

*libarchive* uses [nose](https://nose.readthedocs.org) for testing::

    tests$ ./run.py
