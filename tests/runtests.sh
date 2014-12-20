#!/bin/sh
export PYTHONPATH="../src"
export DJANGO_SETTINGS_MODULE='settings'
export TESTRUNNER=debug_discover_runner.DebugDiscoverRunner

if [ `which django-admin.py` ] ; then
    export DJANGO_ADMIN=django-admin.py
else
    export DJANGO_ADMIN=django-admin
fi

export args="$@"
if [ -z $args ] ; then
    # avoid running the tests for django.contrib.* (they're in INSTALLED_APPS)
    export args=myapp
fi

export DEBUG_RESUME_GRIFFIN=1

$DJANGO_ADMIN test \
    --traceback \
    --settings=$DJANGO_SETTINGS_MODULE \
    --verbosity 3 \
    --pythonpath="./" \
    "$args"
