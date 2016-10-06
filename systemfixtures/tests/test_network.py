import requests

from testtools import TestCase

from ..network import FakeNetwork


class FakeGroupsTest(TestCase):

    def setUp(self):
        super(FakeGroupsTest, self).setUp()
        self.network = self.useFixture(FakeNetwork())

    def test_get(self):
        self.network.get('http://test.com', text='data')
        response = requests.get('http://test.com')
        self.assertEqual("data", response.text)
