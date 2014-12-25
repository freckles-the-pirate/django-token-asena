if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.contrib.auth.models import User, UserManager

from unittest import skip
from datetime import date

import logging, pprint, os
logger = logging.getLogger('test_logger')

from asena.models import token

class TestToken(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create() 
        self.user.username='test_user'

    def test_manual_token_set(self):
        """ A single token can be generated and (semi-)manually added to a token
        set.
        """
        ts = token.TokenSet.objects.create(name="Test Token Set")
        t = token.Token.generate(10, ts, comment="First Token")
        self.assertEqual(len(token.Token.objects.all()), 1)
        t1 = token.Token.objects.get(pk=t.pk)
        self.assertEqual(len(t1.value), 10)
        
    def _test_token_set(self):
        """ A token set can generate many tokens.
        """
        ts = token.TokenSet.generate_set(5, name="Test Token Set")
        self.assertEquals(len(ts.tokens.all()), 5)
        return ts
    
    def test_token_set_unique(self):
        """ A token set can generate UNIQUE tokens.
        """
        ts = self._test_token_set()
        values = []
        for t in ts.tokens.all():
            self.assertNotIn(t.value, values)
            values.append(t.value)