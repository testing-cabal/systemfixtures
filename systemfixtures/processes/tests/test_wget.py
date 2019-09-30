from testtools import TestCase
from testtools.matchers import FileContains

from fixtures import TempDir

from ..wget import Wget


class WgetTest(TestCase):

    def setUp(self):
        super(WgetTest, self).setUp()
        self.locations = {"http://x": b"data"}
        self.wget = Wget(locations=self.locations)

    def test_to_stdout(self):
        result = self.wget({"args": ["wget","-N", "-O", "-", "http://x"]})
        self.assertEqual(b"data", result["stdout"].getvalue())

    def test_to_file(self):
        temp_dir = self.useFixture(TempDir())
        path = temp_dir.join("output")
        self.wget({"args": ["wget", "-N", "-O", path, "http://x"]})
        self.assertThat(path, FileContains("data"))

    def test_to_default(self):
        temp_dir = self.useFixture(TempDir())
        path = temp_dir.join("")
        file_path = temp_dir.join("x")
        print("rootdir: {}".format(path))
        self.wget({"args": ["wget", "-N", "http://x"]}, cwd=path)
        self.assertThat(file_path, FileContains("data"))
