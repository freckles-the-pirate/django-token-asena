if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.test import Client
from django.contrib.auth.models import User, UserManager

from unittest import skip
from datetime import date

import logging, pprint, os
logger = logging.getLogger('test_logger')

from asena.models import *

class TestToken(unittest.TestCase):

    def setUp(self):
        self.user = User.objects.create() 
        self.user.username='test_user'

    def test_manual_token_set(self):
        """ A single token can be generated and (semi-)manually added to a token
        set.
        """
        ts = TokenSet.objects.create(name="Test Token Set")
        t = Token.generate(10, ts, comment="First Token")
        self.assertEqual(len(Token.objects.all()), 1)
        t1 = Token.objects.get(pk=t.pk)
        self.assertEqual(len(t1.value), 10)
        
    def test_tokenset_delete(self):
        """ TokenSets and their respective tokens can be deleted.
        """
        ts = TokenSet.objects.create(name="Test Token Set")
        tokens = [
            Token.generate(10, token_set=ts, comment="First Token").pk,
            Token.generate(10, token_set=ts, comment="First Token").pk,
        ]
        
        test_pk = ts.pk
        self.assertEqual(TokenSet.objects.filter(pk=test_pk).count(), 1)
        for t in tokens:
            self.assertEqual(Token.objects.filter(pk=t).count(), 1)
        TokenSet.objects.filter(pk=test_pk).delete()
        
        self.assertEqual(TokenSet.objects.filter(pk=test_pk).count(), 0)
        for t in tokens:
            self.assertEqual(Token.objects.filter(pk=t).count(), 0)
        
    def _test_token_set(self):
        """ A token set can generate many tokens.
        """
        ts = TokenSet.generate_set(5, name="Test Token Set")
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
    
    """
    " Session testing
    """
    
    def test_get_session_timeout(self):
        """ A token can set a session timeout time based on the token's
        or the token set's timeout.
        """
        ts = TokenSet.objects.create(name="Test Token Set",
                                     session_timeout='0,4')
        token = Token.generate(10, token_set=ts)
        
        expected = datetime.now() + timedelta(hours=0, minutes=4)
        result = token.get_session_expiration(datetime.now())
        
        # We don't care about microseconds (tests will fail if we do!)
        expected = tuple(expected.timetuple())[:5]
        result = tuple(result.timetuple())[:5]
        
        self.assertEqual(expected, result)