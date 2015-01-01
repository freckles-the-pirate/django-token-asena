if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.test.utils import setup_test_environment
from django.test import Client
from django.conf import settings

from unittest import skip
from datetime import date
import string

import logging, pprint, os
logger = logging.getLogger('to_terminal')

from asena import widgets
from asena.forms import TokenCreationForm
from asena.utils import random_chars
from asena.models import token
from django.shortcuts import render

class TestFormElements(unittest.TestCase):
    
    HTML_OUT='./widget.html'
    
    def setUp(self):
        self.token_widget = widgets.TokenWidget()
        
    def testTokenWidget(self):
        name="token_generator_text"
        value=""
        attrs={}
        token_html = self.token_widget.render(name, value, attrs)
        with open(self.HTML_OUT, 'w+') as html_out:
            html_out.write(token_html)
            html_out.close()
    
    def test_token_creation_form(self):
        charset = string.digits + string.ascii_letters
        text = random_chars(charset, 10)
        form = TokenCreationForm({'token_text' : text })
        #logger.debug("Form: %s"%str(form.as_p()))
        self.assertIn(text, form.as_p())