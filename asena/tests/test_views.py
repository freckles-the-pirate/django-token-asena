if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.test.utils import setup_test_environment
from django.test import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from unittest import skip
from datetime import date

import logging, pprint, os
logger = logging.getLogger('to_terminal')

from asena import views
from asena.models import token
from django.shortcuts import render

class TestViews(unittest.TestCase):

    def setUp(self):
        ts = token.TokenSet.objects.create()
        self.test_token = token.Token.generate(token_set=ts,
                                               length=10)
        self.token_key = token.Token._REQUEST_KEY
        setup_test_environment()
        self.client = Client()
        
    def test_token_ajax_request(self):
        """ Token text can be generated from a view.
        """
        token_text = self.client.get(reverse('generate_token', args=[7]))
        self.assertEqual(len(token_text.content), 7)
        self.assertEqual(token_text.status_code/100, 2)

    def test_prompt1(self):
        """ No token is given in a post request and a token wall is produced.
        """
        setup_test_environment()
        client = Client()
        response = client.get(reverse('token_wall'),
                              token_text=self.test_token.value)
        logger.debug(response)
        
    def test_prompt2(self):
        """ A token is given and is valid.
        """
        pass