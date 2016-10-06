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
        result = self.wget({"args": ["wget", "-O", "-", "http://x"]})
        self.assertEqual(b"data", result["stdout"].getvalue())

    def test_to_file(self):
        temp_dir = self.useFixture(TempDir())
        path = temp_dir.join("output")
        self.wget({"args": ["wget", "-O", path, "http://x"]})
        self.assertThat(path, FileContains("data"))
