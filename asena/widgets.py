from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import mark_safe
from django.templatetags.static import static
from django.conf import settings

from asena.utils import html_attrs

import logging, pprint, os
logger = logging.getLogger('to_terminal')

""" Constant to pass in to the "onClick" HTML attribute for a button
"""
ONCLICK_BUTTON_METHOD='generateAsenaToken(%(name)s")'

class Button(forms.Widget):
    def __init__(self, attrs):
        self.attrs = attrs
        self.label = attrs.pop('label', None)
        self.on_click_method = attrs.pop('onClick', none)
        
    def render(self, name, value, attrs=None):
        return mark_safe("<button " +
            html_attrs(attrs) +
            self.on_click_method%{'name' : name} +
            ">" +
            _(self.label) +
            "</button>")

class TokenWidget(forms.MultiWidget):
    
    widgets = [forms.TextInput(attrs={'disabled' : '1'}),
               forms.NumberInput(),
               Button(attrs={'onClick' : ONCLICK_BUTTON_METHOD,}),
               ]
    
    def decompress(self, value):
        return str(value)