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

from asena import widgets
from asena.models import token
from django.shortcuts import render

class TestFormElements(unittest.TestCase):
    
    HTML_OUT='./widget.html'
    
    def setUp(self):
        self.token_widget = widgets.TokenWidget()
        
        # Write the static files to HTML_OUT
        
        
    def testTokenWidget(self):
        name="token_generator_text"
        value=""
        attrs={}
        token_html = self.token_widget.render(name, value, attrs)
        with open(self.HTML_OUT, 'w+') as html_out:
            html_out.write(token_html)
            html_out.close()