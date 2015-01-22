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
from asena.forms import *
from asena.utils import *
from asena.models import *
from asena.fields import *

class TestFormElements(unittest.TestCase):
    
    HTML_OUT = os.path.join(os.path.dirname(__file__),
                            'widget.html')
    STATIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'static')
    TEST_TEMPLATE_DIR = os.path.join(os.path.dirname(__file__),
                                'templates')
    BASIC_TEMPLATE=os.path.join(TEST_TEMPLATE_DIR,
                                'basic.html')
    FORM_TEMPLATE=os.path.join(TEST_TEMPLATE_DIR,
                                'testform.html')
    
    def setUp(self):
        self.token_widget = widgets.TokenWidget()
        
    def test_timedelta_compression(self):
        """ Compression  and decompression works for arbitrary lists, even if 
            None values are used.
        """
        tdf = TimeDeltaField()
        tdw = TimeDeltaWidget()
        test_times = (
            ([1, 2], "1,2", [1, 2], ),
            ([ 5 ], "5,0", [5, 0], ),
            ([5, ], "5,0", [5, 0], ),
            ([None, 5], "0,5", [0, 5], ),
            ([5, None], "5,0", [5, 0], ),
            # We don't test where len > 3 because Django already takes care
            # of that.
        )
        for t in test_times:
            compressed = tdf.compress(t[0])
            decompressed = tdw.decompress(t[1])
            self.assertEqual(compressed, t[1])
            self.assertEqual(decompressed, t[2])
    
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
        logger.info("Widget written to %s"%outfile_path)
        
    def test_token_set_form(self):
        form = TokenSetCreationForm()
        js = [
            'file://' + os.path.abspath(os.path.join(settings.STATIC_ROOT, 
                'tokenGeneration.js')),
            ]
        context = {'scripts' : js, 'body' : form.as_p(), }
        self._write_template(self.FORM_TEMPLATE, context, self.HTML_OUT)
        
    def test_token_wall(self):
        """ The token wall is able to verify a token and authenticate the user.
        Ensure the session token is valid.
        """
        token_set = TokenSet.objects.create()
        token = Token.generate(10, token_set)
        token_wall = TokenWall({'token' : token.value,})
        if not token_wall.is_valid():
            logger.error(pprint.pformat(token_wall.errors))
        self.assertTrue(token_wall.is_valid())
        self.assertIsNotNone(token_wall.get_token())
        
    def test_time_delta_widget(self):
        """
        " A TimeDeltaWidget can be created.
        """
        tdw = TimeDeltaWidget()
        rendered = tdw.render('test_time_delta_widget', '0,10')
        self.assertIsNotNone(rendered)
        logger.debug("Rendered TimeDeltaWidget: %s"%rendered)
        
    def test_time_delta_field(self):
        """
        " A TimeDeltaField can be created.
        """
        tdf = TimeDeltaField()