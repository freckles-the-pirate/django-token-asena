from django import forms
from asena.models import token

class TokenWall(forms.Form):
    token = forms.CharField(label="Token Text")