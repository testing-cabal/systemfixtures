import os
import socket
import subprocess

from testtools import TestCase
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
        self.executable.listen(6666)
        self.executable.out("hello")
        process = subprocess.Popen(
            [self.executable.path], stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        self.addCleanup(process.wait)
        self.addCleanup(process.kill)
        # This ensures that the port will be open
        self.assertEqual(b"hello\n", process.stdout.read(6))
        sock = socket.socket()
        sock.connect(("127.0.0.1", self.executable.port))
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
