from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import mark_safe

import logging, pprint, os
from asena.logger_setup import CONFIG
logger = logging.getLogger('to_terminal')

class TokenWidget(forms.TextInput):
    
    def __init__(self, attrs={}, token_generator_attrs={}):
        attrs.update({  'length' : 20,
                        'title' : 'Token',
                        'disabled' : '1' })
        self.token_generator_attrs = token_generator_attrs
        super(TokenWidget, self).__init__(attrs)
        
    def render(self, name, value, attrs):
        render_fragment = open()