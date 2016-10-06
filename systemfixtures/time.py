from fixtures import Fixture

from fakesleep import (
    monkey_patch,
    monkey_restore,
)


class FakeTime(Fixture):
    """Fixture adapter around fakesleep."""

    def _setUp(self):
        monkey_patch()
        self.addCleanup(monkey_restore)
