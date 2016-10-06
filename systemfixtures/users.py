import pwd

from fixtures import Fixture

from ._overlay import Overlay


class FakeUsers(Fixture):

    def _setUp(self):
        self._users = {}
        self.useFixture(Overlay("pwd.getpwnam", self._getpwnam, self._is_fake))

    def add(self, name, uid):
        self._users[name] = (
            "x", uid, uid, name, "/home/{}".format(name), "/bin/bash")

    def _getpwnam(self, real, name):
        return pwd.struct_passwd((name,) + self._users[name])

    def _is_fake(self, name):
        return name in self._users
