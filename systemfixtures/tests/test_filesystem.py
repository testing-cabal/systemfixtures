import os
import six
import shutil

from testtools import TestCase, skipIf
from testtools.matchers import (
    DirExists,
    HasPermissions,
    FileContains,
)

from fixtures import TempDir

from ..filesystem import FakeFilesystem
from ..matchers import HasOwnership


if six.PY2:
    PermissionError = OSError


class FakeFilesystemTest(TestCase):

    def setUp(self):
        super(FakeFilesystemTest, self).setUp()
        self.fs = self.useFixture(FakeFilesystem())

    def test_add(self):
        self.fs.add("/foo/bar")
        os.makedirs("/foo/bar")
        self.assertThat("/foo/bar", DirExists())

    def test_add_sub_paths(self):
        self.fs.add("/foo")
        os.makedirs("/foo/bar")
        self.assertThat("/foo/bar", DirExists())

    def test_add_non_absolute(self):
        self.assertRaises(ValueError, self.fs.add, "foo/bar")

    def test_fchown(self):
        self.fs.add("/foo/bar")
        os.mkdir("/foo")
        with open("/foo/bar", "w") as fd:
            os.fchown(fd.fileno(), 123, 456)
        self.assertThat("/foo/bar", HasOwnership(123, 456))

    @skipIf(os.getuid() == 0, "Can't run as root")
    def test_fchown_real(self):
        temp_dir = self.useFixture(TempDir())
        path = temp_dir.join("foo")
        with open(path, "w") as fd:
            self.assertRaises(
                PermissionError, os.fchown, fd.fileno(), 12345, 9999)

    def test_chown(self):
        self.fs.add("/foo/bar")
        os.makedirs("/foo/bar")
        os.chown("/foo/bar", 123, 456)
        self.assertThat("/foo/bar", HasOwnership(123, 456))

    @skipIf(os.getuid() == 0, "Can't run as root")
    def test_chown_real(self):
        temp_dir = self.useFixture(TempDir())
        path = temp_dir.join("foo")
        os.makedirs(path)
        self.assertRaises(PermissionError, os.chown, path, 12345, 9999)

    def test_chmod(self):
        self.fs.add("/foo")
        with open("/foo", "w") as fd:
            fd.write("")
        os.chmod("/foo", 0o600)
        self.assertThat("/foo", HasPermissions("0600"))

    def test_symlink(self):
        self.fs.add("/foo")
        os.mkdir("/foo")
        with open("/foo/bar", "w") as fd:
            fd.write("hello")
        os.symlink("/foo/bar", "/foo/egg")
        self.assertThat("/foo/egg", FileContains("hello"))

    def test_unlink(self):
        self.fs.add("/foo")
        os.mkdir("/foo")
        with open("/foo/bar", "w") as fd:
            fd.write("hello")
        os.unlink("/foo/bar")
        self.assertEqual([], os.listdir("/foo"))

    def test_rmtree(self):
        self.fs.add("/foo")
        os.makedirs("/foo/bar/egg")
        shutil.rmtree("/foo/bar")
        self.assertEqual([], os.listdir("/foo"))

    if six.PY3:

        def test_listdir_with_fd(self):
            self.fs.add("/foo")
            os.makedirs("/foo/bar")
            fd = os.open("/foo", os.O_RDONLY)
            self.addCleanup(os.close, fd)
            self.assertEqual(["bar"], os.listdir(fd))

    def test_readlink_to_real_path(self):
        self.fs.add("/foo")
        os.mkdir("/foo")
        temp_dir = self.useFixture(TempDir())
        os.symlink(temp_dir.path, "/foo/bar")
        self.assertEqual(temp_dir.path, os.readlink("/foo/bar"))

    def test_readlink_to_fake_path(self):
        self.fs.add("/foo")
        os.mkdir("/foo")
        os.symlink("/foo/bar", "/foo/egg")
        self.assertEqual("/foo/bar", os.readlink("/foo/egg"))
