from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.text import mark_safe
from django.templatetags.static import static
from django.conf import settings

import logging, pprint, os
logger = logging.getLogger('to_terminal')

class TokenWidget(forms.TextInput):
    
    def __init__(self, attrs={}, token_generator_attrs={}):
        attrs.update({  'length' : 20,
                        'title' : 'Token',
                        'disabled' : '1' })
        self.token_generator_attrs = token_generator_attrs
        super(TokenWidget, self).__init__(attrs)
        
    def render(self, name, value, attrs):
        here = os.path.abspath(os.path.dirname(__file__))
        fragment_path = os.path.join(here, 'fragments',
                                     'token_input.html')
        with open(fragment_path) as render_fragment:
            html = render_fragment.read()
            
        text_name = "%s"%name
        size_name = "%s_size"%name
        generate_name = "%s_generate"%name
        
        token_gen_js = static('tokenGeneration.js')
            
        html = html.format(name=name,
                           value=value,
                           text_name=text_name,
                           size_name=size_name,
                           generate_name=generate_name,
                           token_gen_js=token_gen_js)
        
        return mark_safe(html)