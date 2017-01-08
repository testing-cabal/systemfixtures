import os
import socket

import six

from testtools.content import Content
from testtools.content_type import UTF8_TEXT

from fixtures import (
    Fixture,
    TempDir,
)

if six.PY2:
    import subprocess32 as subprocess
if six.PY3:
    import subprocess


class FakeExecutable(Fixture):
    """Create Python scripts that mimic the behavior of real executables."""

    def _setUp(self):
        self.path = self.useFixture(TempDir()).join("executable")
        self.line("#!/usr/bin/env python")
        self.line("import logging")
        self.line("logging.basicConfig("
                      "format='%(asctime)s %(message)s', level=logging.DEBUG)")
        os.chmod(self.path, 0o0755)

        self._process = None
        self.addDetail("fake-process", Content(UTF8_TEXT, self._process_info))

    def spawn(self):
        """Spawn the fake executable using subprocess.Popen."""
        self._process = subprocess.Popen(
            [self.path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.addCleanup(self._process_kill)

    def out(self, text):
        self.line("import sys")
        self.line("sys.stdout.write('{}\\n')".format(text))
        self.line("sys.stdout.flush()")

    def log(self, message):
        self.line("logging.info('{}')".format(message))

    def sleep(self, seconds):
        self.line("import time")
        self.line("time.sleep({})".format(seconds))

    def hang(self):
        self.line("import time")
        self.line("import signal")
        self.line("signal.signal(signal.SIGTERM, lambda *args: None)")
        self.out("hanging")
        self.line("while True: time.sleep(1)")

    def listen(self, port=None):
        """Make the fake executable listen to the specified port.

        Possible values for 'port' are:

        - None: Allocate immediately a free port and instruct the fake
          executable to use it when it's invoked. This is subject to
          a race condition, if that port that was free when listen() was
          invoked later becomes used before the fake executable had chance
          to bind to it. However it has the advantage of exposing the
          free port as FakeExecutable.port instance variable, that can easily
          be consumed by tests.

        - An integer: Listen to this specific port.
        """
        if port is None:
            port = allocate_port()
        self.port = port
        self.line("import socket")
        self.line("sock = socket.socket()")
        self.line("sock.bind(('localhost', {}))".format(self.port))
        self.log("listening: %d" % self.port)
        self.line("sock.listen(0)")

    def line(self, line):
        with open(self.path, "a") as fd:
            fd.write("{}\n".format(line))

    def _process_kill(self):
        """Kill the fake executable process if it's still running."""
        if self._process.poll() is None:  # pragma: no cover
            self._process.kill()
            self._process.wait(timeout=5)

    def _process_info(self):
        """Return details about the fake process."""
        if not self._process:
            return []

        output, error = self._process.communicate(timeout=5)
        if error is None:
            error = b""
        output = output.decode("utf-8").strip()
        error = error.decode("utf-8").strip()
        info = (u"returncode: %r\n"
                u"output:\n%s\n"
                u"error:\n%s\n" % (self._process.returncode, output, error))
        return [info.encode("utf-8")]


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
