if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.contrib.auth.models import User, UserManager

from unittest import skip
from datetime import date

import logging, pprint, os
logger = logging.getLogger('test_logger')

from asena.utils import *
import string

class TestUtils(unittest.TestCase):
    
    def test_generate(self):
        """ A set of characters can be randomly selected.
        """
        s = random_chars(str(string.letters + string.digits), 10)
        self.assertEquals(len(s), 10)
        print(s)