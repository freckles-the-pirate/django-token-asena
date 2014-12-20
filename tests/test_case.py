if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from unittest import skip

import logging, pprint, os
logger = logging.getLogger('test_logger')

from models.contactfield import *
from models.entity import *

class TestResume(unittest.TestCase):
    def test_assertion(self):
        """ Test that assertions work.
        """
        self.assertTrue(True)
