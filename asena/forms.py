from django import forms
from asena.models import token
from asena.fields import *
from .widgets import *

class TokenWall(forms.Form):
    token = forms.CharField(label="Token Text")
    
class TokenForm(forms.Form):
    pass
    #token_text = forms.CharField(widget=)
        
class TokenSetForm(forms.ModelForm):
    class Meta:
        model = token.TokenSet