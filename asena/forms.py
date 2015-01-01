from django import forms
from django.utils.translation import ugettext_lazy as _
from asena.models import token
from asena.fields import *
from asena.widgets import *

class TokenWall(forms.Form):
    token = forms.CharField(label="Token Text")
    
    def clean(self):
        cleaned_data = super(TokenWall, self).clean()
        token_text = cleaned_data['token']
        ve = forms.ValidationError(
            _("The token %s isn't valid."),
            code='invalid')
        if (token.Token.is_disabled(token_text) or 
            token.Token.is_valid(token_text) ):
                raise ve
        
    
class TokenCreationForm(forms.Form):
    token_text = forms.CharField(widget=TokenWidget())
    
    def clean(self):
        cleaned_data = super(TokenCreationForm, self).clean()
        return cleaned_data
        
class TokenSetForm(forms.ModelForm):
    class Meta:
        model = token.TokenSet