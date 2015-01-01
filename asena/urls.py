from django.conf.urls import *  # NOQA
from django.conf.urls.i18n import i18n_patterns

import asena.views

urlpatterns = patterns('',
    url(r'^token_wall/$', asena.views.token_wall, name="token_wall"),
    url(r'^generate/(?P<length>\d+)$', asena.views.token_ajax_generate, 
        name="generate_token"),
)