import unittest
import os
import snapsnare
from pathlib import Path
from snapsnare.system import utils

from snapsnare.system import utils


class TestUtils(unittest.TestCase):

    def test_lookup(self):

        properties = {
            'current.dir': os.path.abspath(os.getcwd()),
            'package.dir': os.path.dirname(snapsnare.__file__),
            'home.dir': str(Path.home()),
            'app.name': 'snapsnare'
        }

        print(utils.lookup(properties, 'snapsnare-ds.json'))
        print(utils.lookup(properties, 'base_test.py'))
        print(utils.lookup(properties, '/home/jan/workspace/snapsnare/tests/base_test.py'))


if __name__ == '__main__':
    unittest.main()
