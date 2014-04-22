Introduction
------------

A ctypes-based adapter to libarchive. The source-code is written to be clear 
and intuitive.

Even 7-Zip is supported for both reading and writing.

I could definitely use some help, if any is available. Completeness will 
require a bit more work (see *libarchive*'s archive.h).


Installation
------------

PyPI:

```
sudo pip install libarchive
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
|   | Populate archive hosted in memory buffer |
|   | Populate archive entries from memory buffers |
|   | Fill-out the entry object's information/accessors |


Examples
--------

To enumerate the entries in an archive:

```python
import libarchive

with libarchive.reader('test.7z') as reader:
    for e in reader:
        # (The entry evaluates to a filename.)
        print("> %s" % (e))
```

To extract the entries from an archive to the current directory (like a normal,
Unix-based extraction):

```python
import libarchive

for state in libarchive.pour('test.7z'):
    if state.pathname == 'dont/write/me':
        state.set_selected(False)
        continue

    # (The state evaluates to a filename.)
    print("Writing: %s" % (state))
```

To build an archive from a collection of files (omit the target for *stdout*):

```python
import libarchive

for entry in libarchive.create(
                '7z', 
                ['/aa/bb', '/cc/dd'], 
                'create.7z'):
    print("Adding: %s" % (entry))
```
