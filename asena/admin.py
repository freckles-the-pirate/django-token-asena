from django.contrib import admin
from asena.models import token

@admin.register(token.Token)
class TokenAdmin(admin.ModelAdmin):
    pass
@admin.register(token.TokenSet)
class TokenSetAdmin(admin.ModelAdmin):
    pass