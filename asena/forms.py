from django import forms
from django.utils.translation import ugettext_lazy as _
from asena.models import token
from asena.widgets import TokenWidget
from asena.fields import TokenField, TokenSetField

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
    token_name = forms.CharField()
    token_text = TokenField()
    
    def clean(self):
        cleaned_data = super(TokenCreationForm, self).clean()
        return cleaned_data
        
class TokenSetCreationForm(forms.Form):
    count = forms.IntegerField(label="Number of tokens")
    length = forms.IntegerField(label="Length of each token")
    comment = forms.CharField(label="Comment")
    token_set = TokenSetField()
    class Meta:
        model = token.TokenSet