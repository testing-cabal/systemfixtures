import io
import subprocess

from testtools import TestCase

from ..fixture import FakeProcesses


class FakeProcessesTest(TestCase):

    def setUp(self):
        super(FakeProcessesTest, self).setUp()
        self.processes = self.useFixture(FakeProcesses())

    def test_real(self):
        self.assertEqual(b"hi\n", subprocess.check_output(["echo", "hi"]))

    def test_fake(self):

        def get_info(proc_args):
            return {"stdout": io.BytesIO(b"hi!")}

        self.processes.add(get_info, name="echo")
        self.assertIs(get_info, self.processes.echo)
        self.assertEqual(b"hi!", subprocess.check_output(["echo", "hi"]))
