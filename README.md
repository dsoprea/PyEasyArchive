Introduction
------------

A ctypes-based adapter to libarchive. The source-code is written to be clear 
and intuitive.

Even 7-Zip is supported for both reading and writing.

I could definitely use some help, if any is available. Completeness will 
require a bit more work (see *libarchive*'s archive.h and archive_entry.h).


Installation
------------

PyPI:

```
sudo pip install libarchive
```


Notes
-----

The Ubuntu *libarchive* package maintainer refuses to place a "libarchive.so" 
symlink, so you'll have to place this yourself. Depending on your Ubuntu, this 
can be libarchive.so.12, libarchive.so.13, or libarchive.so.14 .

For example:

```
/usr/lib/x86_64-linux-gnu$ sudo ln -s libarchive.so.12 libarchive.so
```


Task List
---------

| Done | Task |
|:----:| ---- |
| X | Read entries from physical file |
| X | Read entries from archive hosted in memory buffer |
| X | Write physical files from archive |
| X | Load memory buffer from archive |
| X | Populate physical archive from physical files |
| X | Populate archive hosted in memory buffer |
|   | Populate archive entries from memory buffers |
|   | Fill-out the entry object's information/accessors |


Examples
--------

To extract to the current directory from a physical file (and print each 
relative filepath):

```python
import libarchive

for entry in libarchive.file_pour('/tmp/test.zip'):
    print(e)
```

To extract to the current directory from memory:

```python
import libarchive

with open('/tmp/test.zip', 'rb') as f:
    for entry in libarchive.memory_pour(f.read()):
        print(e)
```

To read files from a physical archive:

```python
import libarchive

with libarchive.file_reader('test.7z') as e:
    for entry in e:
        with open('/tmp/' + str(entry), 'wb') as f:
            for block in entry.get_blocks():
                f.write(block)
```

To read files from memory:

```python
import libarchive

with open('test.7z', 'rb') as f:
    buffer_ = f.read()
    with libarchive.memory_reader(buffer_) as e:
        for entry in e:
            with open('/tmp/' + str(entry), 'wb') as f:
                for block in entry.get_blocks():
                    f.write(block)
```

To create a physical archive from physical files:

```python
import libarchive

for entry in libarchive.create(
                '7z', 
                ['/etc/profile'], 
                'create.7z'):
    print(entry)
```

To create an archive in memory from physical files:

```python
with open('/tmp/new.7z', 'wb') as f:
    def writer(buffer_, length):
        f.write(buffer_)
        return length

    for entry in libarchive.create_generic(
                    writer,
                    format_name='7z', 
                    files=['/etc/profile']):
        print(entry)
```

Testing
-------

*libarchive* uses [nose](https://nose.readthedocs.org) for testing.

```
tests$ ./run.py
```
