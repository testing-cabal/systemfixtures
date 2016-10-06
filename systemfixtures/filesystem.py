import os
import six

from fixtures import (
    Fixture,
    TempDir,
)

from ._overlay import Overlay

if six.PY2:
    BUILTIN_OPEN = "__builtin__.open"
if six.PY3:
    BUILTIN_OPEN = "builtins.open"


GENERIC_APIS = (
    BUILTIN_OPEN,
    "os.mkdir",
    "os.rmdir",
    "os.chmod",
    "os.remove",
    "os.unlink",
    "os.listdir",
    "os.open",
    "os.path.exists",
    "os.path.isdir",
)


class FakeFilesystem(Fixture):
    """A transparent overlay test filesystem tree.

    It allows to transparently redirect filesystem APIs to a temporary
    directory, instead of the actual filesystem.
    """

    def _setUp(self):
        self.root = self.useFixture(TempDir())
        self._paths = {}
        self._ownership = {}

        if six.PY2:
            # Python 2 doesn't support a fd argument
            condition = self._is_fake_path
        if six.PY3:
            condition = self._is_fake_path_or_fd

        for api in GENERIC_APIS:
            self.useFixture(Overlay(api, self._generic, condition))

        self.useFixture(Overlay("os.fchown", self._fchown, self._is_fake_fd))
        self.useFixture(Overlay("os.chown", self._chown, self._is_fake_path))
        self.useFixture(Overlay("os.stat", self._stat, self._is_fake_path))
        self.useFixture(Overlay("os.lstat", self._stat, self._is_fake_path))
        self.useFixture(Overlay(
            "os.symlink", self._symlink, self._is_fake_symlink))
        self.useFixture(
            Overlay("os.readlink", self._readlink, self._is_fake_path))

    def add(self, path):
        """Add a path to the overlay filesytem.

        Any filesystem operation involving the this path or any sub-paths
        of it will be transparently redirected to temporary root dir.

        @path: An absolute path string.
        """
        if not path.startswith(os.sep):
            raise ValueError("Non-absolute path '{}'".format(path))
        path = path.rstrip(os.sep)
        while True:
            self._paths[path] = None
            path, _ = os.path.split(path)
            if path == os.sep:
                break

    def _fchown(self, real, fileno, uid, gid):
        """Run fake fchown code if fileno points to a sub-path of our tree.

        The ownership set with this fake fchown can be inspected by looking
        at the self.uid/self.gid dictionaries.
        """
        path = self._fake_path(self._path_from_fd(fileno))
        self._chown_common(path, uid, gid)

    def _chown(self, real, path, uid, gid):
        self._chown_common(path, uid, gid)

    def _chown_common(self, path, uid, gid):
        self._ownership[path] = (uid, gid)

    def _stat(self, real, path, *args, **kwargs):
        info = list(real(self._real_path(path)))
        if path in self._ownership:
            info[4:5] = self._ownership[path]
        return os.stat_result(info)

    def _symlink(self, real, src, dst, *args, **kwargs):
        if self._is_fake_path(src):
            src = self._real_path(src)
        if self._is_fake_path(dst):
            dst = self._real_path(dst)
        return real(src, dst, *args, **kwargs)

    def _readlink(self, real, path, *args, **kwargs):
        result = real(self._real_path(path), *args, **kwargs)
        if result.startswith(self.root.path):
            result = self._fake_path(result)
        return result

    def _generic(self, real, path, *args, **kwargs):
        return real(self._real_path(path), *args, **kwargs)

    def _is_fake_path(self, path, *args, **kwargs):
        for prefix in self._paths:
            if path.startswith(prefix):
                return True
        return False

    def _is_fake_fd(self, fileno, *args, **kwargs):
        path = self._path_from_fd(fileno)
        return path.startswith(self.root.path)

    if six.PY3:

        def _is_fake_path_or_fd(self, path, *args, **kwargs):
            if isinstance(path, int):
                path = self._path_from_fd(path)
            return self._is_fake_path(path)

    def _is_fake_symlink(self, src, dst, *args, **kwargs):
        return self._is_fake_path(src) or self._is_fake_path(dst)

    def _path_from_fd(self, fileno):
        return os.readlink("/proc/self/fd/{}".format(fileno))

    def _real_path(self, path):
        return self.root.join(path.lstrip(os.sep))

    def _fake_path(self, path):
        return path[len(self.root.path):]
