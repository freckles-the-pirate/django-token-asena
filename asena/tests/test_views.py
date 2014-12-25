if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.test.utils import setup_test_environment
from django.test import Client

from unittest import skip
from datetime import date

import logging, pprint, os
from asena.logger_setup import CONFIG
logger = logging.getLogger('test_logger')

from asena import views
from asena.models import token
from django.shortcuts import render

class TestViews(unittest.TestCase):

    def setUp(self):
        ts = token.TokenSet.objects.create()
        self.test_token = token.Token.generate(token_set=ts,
                                               length=10)
        self.token_key = token.Token._REQUEST_KEY

    @skip("Reverse URLs not available.")
    def test_prompt(self):
        #setup_test_environment()
        client = Client()
        response = client.get('/', {
            self.token_key : self.test_token.value,
            })
        logger.debug(response)