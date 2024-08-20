import subprocess

from fixtures import FakePopen
from fixtures._fixtures import popen


class FakeProcesses(FakePopen):
    """Enhances FakePopen by supporting multiple processes.

    This is essentially a registry to dispatch calls to FakePopen to
    fake code associated with an executable name, or to fall back to
    real executables in a matching name is not registered.
    """

    def __init__(self):
        self._registry = {}
        self._real_Popen = subprocess.Popen

    def add(self, process, name=None):
        """Add a new process to the registry.

        :param process: A callable (either plain function or object
            implementing __calll).
        :param name: The name of the executable to match. If not given
            it must be provided as 'name' attribute of the given `process`.
            callable.
        """
        name = name or process.name
        assert name, "No executable name given."""
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

    @property
    def args(self):
        return self._args["args"]

    def poll(self):
        return self.returncode

    def communicate(self, input=None, timeout=None):
        return super(_FakeProcessWithMissingAPIs, self).communicate()


popen.FakeProcess = _FakeProcessWithMissingAPIs
