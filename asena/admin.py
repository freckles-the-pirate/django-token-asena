from django.contrib import admin
from asena.models import token

#class TokenAdmin(admin.ModelAdmin):
    #pass

#class TokenSetAdmin(admin.ModelAdmin):
    #pass

admin.site.register(token.TokenSet)
admin.site.register(token.Token)