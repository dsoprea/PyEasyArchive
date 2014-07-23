class ArchiveError(Exception):
    def __init__(self, msg, **kw):
        Exception.__init__(self, msg)
        self.__dict__.update(kw)
