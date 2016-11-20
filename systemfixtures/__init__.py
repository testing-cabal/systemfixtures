import os

from pbr.version import VersionInfo

from .users import FakeUsers
from .groups import FakeGroups
from .filesystem import FakeFilesystem
from .processes import FakeProcesses
from .network import FakeNetwork
from .time import FakeTime
from .threads import FakeThreads
from .executable import FakeExecutable


__all__ = [
    "FakeUsers",
    "FakeGroups",
    "FakeFilesystem",
    "FakeProcesses",
    "FakeNetwork",
    "FakeTime",
    "FakeThreads",
    "FakeExecutable",
]


_v = VersionInfo("systemfixtures").semantic_version()
__version__ = _v.release_string()
version_info = _v.version_tuple()


def load_tests(loader, standard_tests, pattern):
    this_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern=pattern)
    standard_tests.addTests(package_tests)
    return standard_tests
