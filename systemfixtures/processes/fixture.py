import six
import subprocess

from fixtures import FakePopen
from fixtures._fixtures import popen


class FakeProcesses(FakePopen):
    """Enhances FakePopen by supporting multiple processes."""

    def __init__(self):
        self._registry = {}
        self._real_Popen = subprocess.Popen

    def add(self, process, name=None):
        name = name or process.name
        self._registry[name] = process

    def get_info(self, proc_args):
        name = proc_args["args"][0]
        get_info = self._registry[name]
        return get_info(proc_args)

    def __call__(self, *args, **kwargs):
        name = args[0][0]
        if name not in self._registry:
            return self._real_Popen(*args, **kwargs)
        return super(FakeProcesses, self).__call__(*args, **kwargs)

    def __getattr__(self, name):
        return self._registry[name]


class _FakeProcessWithMissingAPIs(popen.FakeProcess):
    """Can be dropped once:

    https://github.com/testing-cabal/fixtures/pull/32.

    is merged upstream.
    """

    if six.PY3:

        @property
        def args(self):
            return self._args["args"]

    def poll(self):
        return self.returncode

    def communicate(self, input=None, timeout=None):
        return super(_FakeProcessWithMissingAPIs, self).communicate()


popen.FakeProcess = _FakeProcessWithMissingAPIs
