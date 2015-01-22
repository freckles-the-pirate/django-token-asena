from django import forms
from asena.widgets import *

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
        return ''

class TimeDeltaField(forms.MultiValueField):
    widget = TimeDeltaWidget

    def __init__(self, *args, **kwargs):

        super(TimeDeltaField, self).__init__( fields = (
            forms.IntegerField(label="Hours"),
            forms.IntegerField(label="Minutes"),
            forms.IntegerField(label="Seconds"),
        ), **kwargs)

    def compress(self, data_list):
        """ Compress the TimeDeltaField. If any fields are left blank,
        fill them in with a zero.
        """
        data = [0]*(3-len(data_list)) + [str(d) for d in data_list]
        logging.debug("Compressing %s -> %s."%(data, data_list))
        return data
