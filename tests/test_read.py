import libarchive

_TEST_READ_ARCHIVE = 'resources/test.7z'

def test_enumerate_from_file():
    with libarchive.file_enumerator(_TEST_READ_ARCHIVE) as e:
        for entry in e:
            print(entry)

def test_enumerate_from_memory():
    with open(_TEST_READ_ARCHIVE, 'rb') as f:
        buffer_ = f.read()
        with libarchive.memory_enumerator(buffer_) as e:
            for entry in e:
                print(entry)

def test_read_from_file():
    with libarchive.file_reader(_TEST_READ_ARCHIVE) as e:
        for entry in e:
            with open('/tmp/' + str(entry), 'wb') as f:
                for block in entry.get_blocks():
                    f.write(block)

def test_read_from_memory():
    with open(_TEST_READ_ARCHIVE, 'rb') as f:
        buffer_ = f.read()
        with libarchive.memory_reader(buffer_) as e:
            for entry in e:
                with open('/tmp/' + str(entry), 'wb') as f:
                    for block in entry.get_blocks():
                        f.write(block)
