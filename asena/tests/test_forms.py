if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from django import test as unittest
from django.test.utils import setup_test_environment
from django.test import Client
from django.conf import settings
from django.shortcuts import render
from django.templatetags.static import static
from django.template import Template, loader
from django.template.context import Context

from unittest import skip
from datetime import date
import string

import logging, pprint, os
logger = logging.getLogger('to_terminal')

from asena import widgets
from asena.forms import TokenCreationForm, TokenSetCreationForm
from asena.utils import random_chars
from asena.models import *

class TestFormElements(unittest.TestCase):
    
    HTML_OUT = './widget.html'
    STATIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'static')
    TEST_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),
                                'templates')
    BASIC_TEMPLATE=os.path.join(TEST_TEMPLATE_DIR,
                                'basic.html')
    FORM_TEMPLATE=os.path.join(TEST_TEMPLATE_DIR,
                                'testform.html')
    
    def setUp(self):
        self.token_widget = widgets.TokenWidget()
    
    @skip("Useless because we need to generate a set.")
    def testTokenWidget(self):
        name="token_generator_text"
        value=""
        attrs={}
        token_html = self.token_widget.render(name, value, attrs)
        with open(self.HTML_OUT, 'w+') as html_out:
            html_out.write(token_html)
            html_out.close()
    
    @skip("Useless because we need to generate a set.")
    def test_token_creation_form(self):
        charset = string.digits + string.ascii_letters
        text = random_chars(charset, 10)
        form = TokenCreationForm()
        form.token_text = text
        self.assertIn(text, form.as_p())
        
    def _write_template(self, template_path, context, outfile_path):
        with open(template_path, 'r') as f:
            source = f.read()
            f.close()
        t = Template(source)
        c = Context(context)
        rendered = t.render(c)
        #logger.debug("Rendered %s"%rendered)
        with open(outfile_path, 'w+') as f:
            f.write(rendered)
            f.close()
        
    def test_token_set_form(self):
        form = TokenSetCreationForm()
        js = [
            'file://' + os.path.abspath(os.path.join(self.STATIC_DIR, 
                'tokenGeneration.js')),
            ]
        context = {'scripts' : js, 'body' : form.as_p(), }
        self._write_template(self.FORM_TEMPLATE, context, self.HTML_OUT)