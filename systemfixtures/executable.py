import os
import socket

from fixtures import (
    Fixture,
    TempDir,
)


SUBSTITUTIONS = {
}


class FakeExecutable(Fixture):
    """Create Python scripts that mimic the behavior of real executables."""

    def _setUp(self):
        self.path = self.useFixture(TempDir()).join("executable")
        self.line("#!/usr/bin/env python")
        os.chmod(self.path, 0o0755)

    def out(self, text):
        self.line("import sys")
        self.line("sys.stdout.write('{}\\n')".format(text))
        self.line("sys.stdout.flush()")

    def sleep(self, seconds):
        self.line("import time")
        self.line("time.sleep({})".format(seconds))

    def hang(self):
        self.line("import time")
        self.line("import signal")
        self.line("signal.signal(signal.SIGTERM, lambda *args: None)")
        self.line("while True: time.sleep(1)")

    def listen(self, port=None):
        if port is None:
            port = allocate_port()
        self.port = port
        self.line("import socket")
        self.line("sock = socket.socket()")
        self.line("sock.bind(('localhost', {}))".format(self.port))
        self.line("sock.listen(0)")

    def line(self, line):
        with open(self.path, "a") as fd:
            fd.write("{}\n".format(line))


def get_port(socket):
    """Return the port to which a socket is bound."""
    addr, port = socket.getsockname()
    return port


def allocate_port():
    """Allocate an unused port.

    There is a small race condition here (between the time we allocate the
    port, and the time it actually gets used), but for the purposes for which
    this function gets used it isn't a problem in practice.
    """
    sock = socket.socket()
    try:
        sock.bind(("localhost", 0))
        return get_port(sock)
    finally:
        sock.close()
