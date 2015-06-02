from django.conf.urls import *  # NOQA
from django.conf.urls.i18n import i18n_patterns
import sys,os

import asena.views

urlpatterns = patterns('',
    url(r'^token_wall/$', asena.views.token_wall, name="token_wall"),
    url(r'^token/generate/(?P<count>\d+)/(?P<length>\d+)/$',
        asena.views.token_set_ajax_generate,
        name="generate_token_set"),
    url(r'^token/generate/(?P<length>\d+)/$', asena.views.token_ajax_generate, 
        name="generate_token"),
)
    
if int(os.environ.get('TEST_ASENA', 0)) == 1:
    sys.path.append(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                '..' )))
    urlpatterns = urlpatterns + patterns('',
        url(r'test/my-view/(?P<x>\d+)/(?P<y>\d+)$',
            'tests.view_tests.my_view', name='my_view'),
    )