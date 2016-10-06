from testtools import TestCase

from ..dpkg import Dpkg


class DpkgTest(TestCase):

    def setUp(self):
        super(DpkgTest, self).setUp()
        self.dpkg = Dpkg()

    def test_install(self):
        self.dpkg({"args": ["dpkg", "-i", "foo_1.0-1.deb"]})
        self.assertEqual(["install"], self.dpkg.actions["foo"])
