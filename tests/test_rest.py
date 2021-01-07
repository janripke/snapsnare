import os
import unittest

from tests.base_test import BaseTestCase
from snapsnare.system.requestors import RestRequest
from snapsnare.system.requestors import BearerRequest


class TestRest(BaseTestCase):

    def auth(self):
        url = '{}/auth'.format(TestRest.ENDPOINT)

        identity = {
            'username': 'admin@computersnaar.nl',
            'password': 'TheRealIngestionFactory'
        }

        proxies = TestRest.REQUESTS_PROXIES

        request = RestRequest(proxies=proxies)
        response = request.post(url, identity)
        content = response.json()
        return content.get('access_token')

    def test_show_property(self):
        access_token = self.auth()

        url = '{}/properties/show?name={}'.format(
            TestRest.ENDPOINT, 'application.environment'
        )

        proxies = TestRest.REQUESTS_PROXIES

        request = BearerRequest(access_token, proxies=proxies)
        response = request.get(url)

        status_code = response.status_code
        expected = 200
        self.assertEqual(expected, status_code, 'invalid status_code')

        content = response.json()
        self.assertIsNotNone(content, 'no content')

        apy = content.get('property')
        environment = apy.get('value')
        self.assertIsNotNone(environment, "no environment")

        expected = os.environ.get('ENVIRONMENT', 'local')
        self.assertEqual(expected, environment,
                         'invalid state, expected {} got {}'.format(expected, environment))


if __name__ == '__main__':
    unittest.main()
