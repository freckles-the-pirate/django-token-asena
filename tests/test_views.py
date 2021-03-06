if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.shortcuts import render
from django.test.utils import setup_test_environment
from django.test import Client
from django.core.urlresolvers import reverse
from django.conf import settings
from django.http import HttpResponse

from unittest import skip
from datetime import date

import logging, pprint, os
logger = logging.getLogger('asena')

from asena import views
from asena.models import *
from asena.utils import *
from asena.forms import *


class TestViews(unittest.TestCase):

    def setUp(self):
        ts = TokenSet.objects.create()
        self.test_token =Token.generate(token_set=ts,
                                               length=10)
        self.token_key = Token._REQUEST_KEY
        setup_test_environment()
        self.client = Client()
        
    
    @skip("Removing option to generate a single token.")
    def test_token_ajax_request(self):
        """ Token text can be generated from a view.
        """
        token_text = self.client.get(reverse('generate_token', args=[7]))
        self.assertEqual(len(token_text.content), 7)
        self.assertEqual(token_text.status_code/100, 2)
        
    def test_token_set_ajax_request(self):
        """ A set of token values can be returned (5 tokens, each with a length 
        of 10).
        """
        count=5
        args=[count, 10]
        url = reverse('generate_token_set', args=args)
        response = self.client.get(url)
        self.assertEqual(response.status_code/100, 2)
        token_set = response.content.split(',')
        logger.debug("Query: %s, Response %s"%(url, token_set))
        self.assertEqual(len(token_set), count)

    def test_prompt1(self):
        """ No token is given in a post request and a token wall is produced.
        """
        setup_test_environment()
        client = Client()
        response = client.get(reverse('token_wall'),
                              token_text=self.test_token.value)
        self.assertEqual(response.status_code, 200)
        
    def test_good_view(self):
        """ The ``@token_protect`` wrapper function allows valid tokens.
        """
        good_url = reverse('my_view', kwargs={'x' : 5, 'y' : 3}) + "?token=%s"%(self.test_token.value)
        response = self.client.get(good_url)
        logger.info("(Good) Response: %s", response.content)
        self.assertEqual(response.content, "5 + 3 is 8")
        
    def test_bad_view(self):
        """ The ``@token_protect`` wrapper function redirects to the token \
        wall on invalid tokens.
        """
        response = self.client.get(reverse('my_view',
                                           kwargs={'x' : 5, 'y' : 3}))
        logger.info("(Bad) Response: %s", response.content)
        self.assertEqual(response.status_code, 200)