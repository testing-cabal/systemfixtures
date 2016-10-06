from fixtures import Fixture

from requests_mock import Mocker


class FakeNetwork(Fixture):
    """Fixture adapter around request-mock."""

    def _setUp(self):
        self._requests = Mocker()
        self._requests.start()
        self.addCleanup(self._requests.stop)

    def __getattr__(self, name):
        return getattr(self._requests, name)
