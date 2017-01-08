import os
import time
import errno
import socket
import logging
import subprocess

from fixtures import FakeLogger

from testtools import TestCase
from testtools.content import text_content
from testtools.matchers import (
    Contains,
    FileContains,
)

from ..executable import FakeExecutable


class FakeExecutableTest(TestCase):

    def setUp(self):
        super(FakeExecutableTest, self).setUp()
        self.executable = self.useFixture(FakeExecutable())

    def test_out(self):
        self.executable.out("hello")
        self.assertEqual(
            b"hello\n", subprocess.check_output([self.executable.path]))

    def test_sleep(self):
        self.executable.sleep(1)
        self.assertThat(
            self.executable.path,
            FileContains(matcher=Contains("time.sleep(1)")))

    def test_listen_random(self):
        self.executable.listen()
        self.assertIsNotNone(self.executable.port)

    def test_listen(self):
        logger = self.useFixture(FakeLogger(format="%(asctime)s %(message)s"))
        self.executable.listen(6666)
        self.executable.sleep(1)
        self.executable.spawn()

        # Try to connect to the socket
        sock = socket.socket()
        transient = (errno.ECONNREFUSED, errno.ECONNRESET)

        attempts = 10
        for i in range(1, attempts + 1):
            try:
                sock.connect(("127.0.0.1", self.executable.port))
            except socket.error as error:  # pragma: no cover
                if error.errno in transient and i != attempts:
                    time.sleep(0.05 * i)
                    continue
                logging.error("connection attempt %d failed", i)
                raise error
            break
        self.assertEqual("127.0.0.1", sock.getsockname()[0])

    def test_hang(self):
        self.executable.out("hello")  # Used to ensure the process is running
        self.executable.hang()
        process = subprocess.Popen(
            [self.executable.path], stdout=subprocess.PIPE)
        self.assertEqual(b"hello\n", process.stdout.read(6))
        process.terminate()
        self.addCleanup(process.wait)
        self.addCleanup(process.kill)
        self.assertEqual((0, 0), os.waitpid(process.pid, os.WNOHANG))
