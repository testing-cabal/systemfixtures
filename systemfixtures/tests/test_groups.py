import grp

from testtools import TestCase

from ..groups import FakeGroups


class FakeGroupsTest(TestCase):

    def setUp(self):
        super(FakeGroupsTest, self).setUp()
        self.groups = self.useFixture(FakeGroups())

    def test_real(self):
        info = grp.getgrnam("root")
        self.assertEqual(0, info.gr_gid)

    def test_fake(self):
        self.groups.add("foo", 123)
        info = grp.getgrnam("foo")
        self.assertEqual(123, info.gr_gid)
