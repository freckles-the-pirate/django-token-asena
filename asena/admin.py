from django.contrib import admin
from asena.models import *
from asena.forms import *

import logging
logger = logging.getLogger('asena')

class TokenAdmin(admin.ModelAdmin):
    form = TokenCreationForm

class TokenSetAdmin(admin.ModelAdmin):
    form = TokenSetCreationForm

admin.site.register(TokenSet, TokenSetAdmin)
admin.site.register(Token, TokenAdmin)
