from django import forms
from asena.widgets import TokenWidget, TokenSetWidget

from django.conf import settings
import logging, pprint, os
logger = logging.getLogger('to_terminal')

class TokenField(forms.MultiValueField):
    #widget = TokenWidget
    
    def __init__(self, *args, **kwargs):
        token_value = kwargs.pop('token_value', None)
        self.widget = TokenWidget(attrs={'token_value' : token_value})
        fields = (forms.CharField(), forms.IntegerField())
        super(TokenField, self).__init__(fields, *args, **kwargs)
    
    def compress(self, data_list):
        logger.debug("Compressing data list %s"%pprint.pformat(data_list))
        if len(data_list) >= 1:
            return data_list[0]
        return None
    
class TokenSetField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.widget = TokenSetWidget()
        fields = (
            forms.MultipleChoiceField(),
        )
        super(TokenSetField, self).__init__(fields, *args, **kwargs)
        
        def compress(self, data_list):
            logger.debug("Compressing data list %s"%pprint.pformat(data_list))
            if len(data_list) > 0:
                return data_list.join(',')