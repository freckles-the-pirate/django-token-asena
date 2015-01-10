#!/bin/sh

if [ -z $PYENV ]; then
    echo "ERRROR: Missing environment variable \`PYENV\` that points to "
    echo "        Python's virtual environment. Please set it and run"
    echo "        \`$0 $*\` again."
    exit
fi

source $PYENV

BASE_TESTING_PATH=$1
BASE_TESTING_MODULE=$(echo $BASE_TESTING_PATH | sed 's/\.\///g' | sed 's/\//\./g')

export PYTHONPATH=$(pwd)

export DJANGO_SETTINGS_MODULE=$BASE_TESTING_MODULE'.tests.settings_test'
#export TESTRUNNER=debug_discover_runner.DebugDiscoverRunner
# Django's new test runner.
export TEST_RUNNER=django.test.runner.DiscoverRunner

if [ `which django-admin.py` ] ; then
    export DJANGO_ADMIN=django-admin.py
else
    export DJANGO_ADMIN=django-admin
fi

export args="$@"
if [ -z $args ] ; then
    # avoid running the tests for django.contrib.* (they're in INSTALLED_APPS)
    export args=my_app
fi

export DEBUG_ASENA=1

# TESTS=$(find $BASE_TESTING_PATH -print | grep -P --color=never 'tests/test_.+\.py$')
TESTS=$(find $BASE_TESTING_PATH -iname 'tests' -print)

echo Tests: $TESTS;

###
# Converts a given shell path (e.g. /path/to/module.py) into a python name
# (e.g. path.to.module)
pypath(){
    echo $( echo $1 | sed 's/\.py//g' | \
        sed 's/\.\///g' | \
        sed 's/\//\./g' )
}

for TEST in $TESTS; do

    # This converts the path into a python module.
    TEST_NAME=$(pypath $TEST)
    
    echo Testing $TEST_NAME

    COMMAND="$DJANGO_ADMIN test \
        --traceback \
        --settings=$DJANGO_SETTINGS_MODULE \
        --verbosity 3 \
        --pythonpath=$PYTHONPATH \
        $TEST_NAME"

    echo $COMMAND
    $COMMAND
done