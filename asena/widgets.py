from django import forms
from django.utils.text import mark_safe
from django.templatetags.static import static
from django.conf import settings

from asena.utils import html_attrs

import logging, pprint, os
logger = logging.getLogger('to_terminal')

""" Constant to pass in to the "onClick" HTML attribute for a button
"""
ONCLICK_BUTTON_METHOD="generateAsenaTokens('%(id)s'); return false;"

""" In case the static URL changes, make it a constant, too
"""
STATIC_JS='tokenGeneration.js'

class Button(forms.Widget):
    def __init__(self, attrs):
        self.attrs = attrs
        self.label = self.attrs.pop('label', '')
        self.on_click_method = attrs.pop('onClick', None)
        
    def render(self, name, value, attrs=None):
        """ Render the button.
        
        If given an ``onClick`` attribute, id of the widget will be passed in to
        the function parameters.
        
        :param name: The name of the widget
        :type name: str
        
        :param value: The value of the widget (unused).
        :type value: void
        
        :param attrs: Attributes for the widget.
        :type attrs: dict
        """
        if 'id' in attrs and self.on_click_method:
            attrs.update({
                'onClick' : str(self.on_click_method%{'id' : attrs['id'],}),
                'type' : 'button',
            })
            
        # It's ugly, but first we need to prepend some javascript.
        js = static(STATIC_JS)
        
        s = """<script type="text/javascript"></script>
<script type="text/javascript" src="%s"></script>"""%js
        
        return mark_safe(s + "<button %s>%s</button>"%(html_attrs(attrs),
                                                   self.label))
    
class SizeWidget(forms.NumberInput):
    def render(self, name, value, attrs):
        html = super(SizeWidget, self).render(name, value, attrs)
        return mark_safe('<label for="%s">Size:</label>%s'%(name, html))

class TokenWidget(forms.MultiWidget):
    
    def __init__(self, attrs={}):
        """ A widget to generate a token.
        
        :param attrs:   attributes for the widget. So far attrs is largely
                        ignored except for the key ``token_value`` wich is the 
                        value of the token we want to generate.
        
        :type attrs:    dict
        """
        logger.debug("Token attributes: %s"%pprint.pformat(attrs))
        token_value = attrs.pop('token_value', None)
        text_attrs = {'disabled' : '1',}
        if token_value:
            text_attrs.update({'value' : token_value,})
        widgets = [forms.TextInput(text_attrs),
                   SizeWidget(),
                   Button(attrs={'onClick' : ONCLICK_BUTTON_METHOD,}),
               ]
        super(TokenWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        if not value:
            return [None,]
        logger.debug("Decompressing value \"%s\""%value)
        return [value,]
    
class TokenSetWidget(forms.MultiWidget):
    def __init__(self, attrs={}):
        button_attrs = {
            'label' : 'Generate',
            'onClick' : ONCLICK_BUTTON_METHOD,
        }
        widgets = (
            forms.SelectMultiple(),
            Button(button_attrs),
        )
        super(TokenSetWidget, self).__init__(widgets, attrs)
    
    def decompress(self, value):
        if not value:
            return [None,]
        logger.debug("Decompressing value \"%s\""%value)
        return [value,]