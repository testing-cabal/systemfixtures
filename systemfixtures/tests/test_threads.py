import threading

from testtools import TestCase

from ..threads import FakeThreads


class FakeThreadsTest(TestCase):

    def setUp(self):
        super(FakeThreadsTest, self).setUp()
        self.threads = self.useFixture(FakeThreads())

    def test_getitem(self):
        thread = threading.Thread()
        self.assertIs(thread, self.threads[0])

    def test_start(self):
        calls = [None]
        thread = threading.Thread(target=calls.pop)
        self.assertFalse(thread.isAlive())
        thread.start()
        self.assertEqual([], calls)
        self.assertFalse(thread.isAlive())

    def test_twice(self):
        thread = threading.Thread(target=lambda: None)
        thread.start()
        error = self.assertRaises(RuntimeError, thread.start)
        self.assertEqual("threads can only be started once", str(error))

    def test_join_before_starting(self):
        thread = threading.Thread()
        error = self.assertRaises(RuntimeError, thread.join)
        self.assertEqual("cannot join thread before it is started", str(error))

    def test_hang(self):
        self.threads.hang()
        thread = threading.Thread()
        thread.start()
        thread.join(timeout=1)
        self.assertTrue(thread.isAlive())

    def test_hang_without_timeout(self):
        self.threads.hang()
        thread = threading.Thread()
        thread.start()
        error = self.assertRaises(AssertionError, thread.join)
        self.assertEqual(
            "can't simulate hung thread with no timeout", str(error))
