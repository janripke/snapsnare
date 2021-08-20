import unittest
import os
from pathlib import Path

from paprika_connector.connectors.connector_factory import ConnectorFactory

import snapsnare
from snapsnare.system import utils
from snapsnare.repositories.activity.activity_repository import ActivityRepository
from snapsnare.repositories.user.user_repository import UserRepository


class TestRepository(unittest.TestCase):
    def test_activity_list(self):
        properties = {
            'current.dir': os.path.abspath(os.getcwd()),
            'package.dir': os.path.dirname(snapsnare.__file__),
            'home.dir': str(Path.home()),
            'app.name': 'snapsnare'
        }

        ds = utils.load_json(properties, 'snapsnare-ds.json')
        connector = ConnectorFactory.create_connector(ds)
        connector.connect()

        activity_repository = ActivityRepository(connector)
        activities = activity_repository.list()

        connector.close()

    def test_user_insert(self):
        properties = {
            'current.dir': os.path.abspath(os.getcwd()),
            'package.dir': os.path.dirname(snapsnare.__file__),
            'home.dir': str(Path.home()),
            'app.name': 'snapsnare'
        }

        ds = utils.load_json(properties, 'snapsnare-ds.json')
        connector = ConnectorFactory.create_connector(ds)
        connector.connect()

        user_repository = UserRepository(connector)

        user = {
            'username': 'test@snapsnare.com',
            'password': 'buiswater'
        }

        id_ = user_repository.insert(user)
        self.assertIsNotNone(id_, 'no id')

        user = user_repository.find_by(id=id_)
        connector.rollback()
        connector.close()

        self.assertIsNotNone(user, 'no user')

        username = user.get('username')
        self.assertIsNotNone(username, 'no username')

        expected = 'test@snapsnare.com'
        self.assertEqual(expected, username,
                         'invalid state, expected {} got {}'.format(expected, username))


if __name__ == '__main__':
    unittest.main()
