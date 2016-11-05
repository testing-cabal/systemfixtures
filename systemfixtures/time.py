from fixtures import Fixture

from fakesleep import (
    monkey_patch,
    monkey_restore,
    reset,
)


class FakeTime(Fixture):
    """Fixture adapter around fakesleep."""

    def set(self, seconds=None):
        """Set the global fake time to the given epoch or the real current one.

        :param seconds: Fake current time, in seconds since the epoch. If
             ``None``, use the real current time.
        """
        reset(seconds=seconds)

    def _setUp(self):
        monkey_patch()
        self.addCleanup(monkey_restore)
