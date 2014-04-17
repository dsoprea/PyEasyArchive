Introduction
------------

A ctypes-based adapter to libarchive. The source-code is written to be clear 
and intuitive.

Even 7-Zip is supported.

**This is a work in progress to be finished very soon.**

I could definitely use some help contributing to the completeness of this
library.


Task List
---------

| Done | Task |
|:----:| ---- |
| X | Enumerate entries |
| X | Extract entries to disk |
|   | Create archives |
|   | Fill-out the entry object's information/accessors |


Examples
--------

To enumerate the entries in an archive:

```python
import libarchive

with libarchive.reader('test.7z') as reader:
    for e in reader:
        print("> %s" % (e))
```

To extract the entries from an archive to the current directory (like a normal,
Unix-based extraction):

```python
import libarchive

for entry in libarchive.pour('test.7z'):
    print("Wrote: %s" % (entry))
```

