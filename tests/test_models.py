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
from asena.utils import *

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

        init = datetime.now()
        
        expected = init + timedelta(hours=0, minutes=4)
        result = token.get_session_expiration(init)
               
        self.assertEqual(expected, result)

    def test_get_session_dict(self):
        """ The session dict is returned giving correct values.
        """
        ts = TokenSet.objects.create(name="Test Token Set",
                                     session_timeout='0,4')
        token = Token.generate(10, token_set=ts)

        init=datetime.now()

        timeout_name = get_default_setting('ASENA_SESSION_TIMEOUT_NAME')
        session_name = get_default_setting('ASENA_SESSION_NAME')
        dt_format = get_default_setting('ASENA_DATETIME_FORMAT')

        expected_dt = (init + timedelta(hours=0, minutes=4)).strftime(
                dt_format)
        
        expected = {
                timeout_name : expected_dt,
                session_name : token.value,
            }

        result = token.get_session()

        self.assertEqual(expected, result)

    def test_session_has_timed_out(self):
        """ The token returns True if the session has expired based on
        the session data.
        """

        timeout_name = get_default_setting('ASENA_SESSION_TIMEOUT_NAME')
        session_name = get_default_setting('ASENA_SESSION_NAME')
        dt_format = get_default_setting('ASENA_DATETIME_FORMAT')

        mock_now = datetime.now() - timedelta(hours=1)
        mock_expiration = datetime.now()
        mock_after = datetime.now() + timedelta(hours=1)

        """ Providing mock data will avoid having to set up a client.
        """
        mock_session_data = {
            session_name : 'random_value',
            timeout_name : mock_expiration.strftime(dt_format),
        }

        self.assertFalse(has_session_expired(mock_session_data, mock_now))
        self.assertTrue(has_session_expired(mock_session_data, mock_after))
        self.assertTrue(has_session_expired({}, mock_after))
        self.assertTrue(has_session_expired(None, mock_after))

    def test_get_time_remaining(self):
        """ The correct time remaining is calculated.
        """
 
        timeout_name = get_default_setting('ASENA_SESSION_TIMEOUT_NAME')
        session_name = get_default_setting('ASENA_SESSION_NAME')
        dt_format = get_default_setting('ASENA_DATETIME_FORMAT')

        now = datetime.now()

        mock_now = now - timedelta(minutes=1)
        mock_expiration = now
        mock_after = now + timedelta(minutes=1)

        expected_now = timedelta(minutes=1).total_seconds()
        expected_expiration = timedelta().total_seconds()
        expected_later = timedelta().total_seconds()

        """ Providing mock data will avoid having to set up a client.
        """
        mock_session_data = {
            session_name : 'random_value',
            timeout_name : mock_expiration.strftime(dt_format),
        }

        tests = (
            (mock_now, expected_now),
            (mock_expiration, expected_expiration),
            (mock_after, expected_later),
            (None, expected_later),
        )

        for t in tests:
            result = get_session_time_remaining(mock_session_data, t[0])
            self.assertEqual(int(result.total_seconds()), t[1])

