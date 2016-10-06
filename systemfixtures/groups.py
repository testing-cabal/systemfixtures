import grp

from fixtures import Fixture

from ._overlay import Overlay


class FakeGroups(Fixture):

    def _setUp(self):
        self._groups = {}
        self.useFixture(Overlay("grp.getgrnam", self._getgrnam, self._is_fake))

    def add(self, name, gid):
        self._groups[name] = ("x", gid, [])

    def _getgrnam(self, real, name):
        return grp.struct_group((name,) + self._groups[name])

    def _is_fake(self, name):
        return name in self._groups
