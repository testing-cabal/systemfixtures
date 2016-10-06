from .fixture import FakeProcesses
from .wget import Wget
from .systemctl import Systemctl
from .dpkg import Dpkg


__all__ = [
    "FakeProcesses",
    "Wget",
    "Systemctl",
    "Dpkg",
]
