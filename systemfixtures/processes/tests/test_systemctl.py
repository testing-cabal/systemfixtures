from testtools import TestCase

from ..systemctl import Systemctl


class SystemctlTest(TestCase):

    def setUp(self):
        super(SystemctlTest, self).setUp()
        self.systemctl = Systemctl()

    def test_stop(self):
        self.systemctl({"args": ["systemctl", "stop", "foo"]})
        self.assertEqual(["stop"], self.systemctl.actions["foo"])

    def test_start(self):
        self.systemctl({"args": ["systemctl", "start", "foo"]})
        self.assertEqual(["start"], self.systemctl.actions["foo"])

    def test_is_active(self):
        self.systemctl({"args": ["systemctl", "start", "foo"]})
        result = self.systemctl({"args": ["systemctl", "is-active", "foo"]})
        self.assertEqual(0, result.get("returncode"))

    def test_is_not_active(self):
        result = self.systemctl({"args": ["systemctl", "is-active", "foo"]})
        self.assertEqual(3, result["returncode"])
