from django.conf.urls import patterns, url

# Make sure you copy this line into the main urls.py:
#   url(r'^app_name/', include(app_name.urls))

urlpatterns = patterns('',
    url(r'^$', 'app_name.views.index'),
)

