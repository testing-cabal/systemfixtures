import pwd

from testtools import TestCase

from ..users import FakeUsers


class FakeUsersTest(TestCase):

    def setUp(self):
        super(FakeUsersTest, self).setUp()
        self.users = self.useFixture(FakeUsers())

    def test_real(self):
        info = pwd.getpwnam("root")
        self.assertEqual(0, info.pw_uid)

    def test_fake(self):
        self.users.add("foo", 123)
        info = pwd.getpwnam("foo")
        self.assertEqual(123, info.pw_uid)
