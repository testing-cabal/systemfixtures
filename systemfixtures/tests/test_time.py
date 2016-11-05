import time

from testtools import TestCase

from ..time import FakeTime


class FakeTimeTest(TestCase):

    def setUp(self):
        super(FakeTimeTest, self).setUp()
        self.time = self.useFixture(FakeTime())

    def test_time(self):
        stamp1 = time.time()
        stamp2 = time.time()
        self.assertEqual(stamp2, stamp1)

    def test_sleep(self):
        stamp1 = time.time()
        time.sleep(1)
        stamp2 = time.time()
        self.assertEqual(1, stamp2 - stamp1)

    def test_reset(self):
        self.time.set(123)
        self.assertEqual(123, time.time())
