import os

from testtools.matchers import (
    AfterPreprocessing,
    Equals,
)


def HasOwnership(uid, gid):

    def ownership(path):
        info = os.stat(path)
        return info.st_uid, info.st_gid

    return AfterPreprocessing(ownership, Equals((uid, gid)))
