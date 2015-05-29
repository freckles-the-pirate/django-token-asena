#!/usr/bin/env python
import os, sys

BASEDIR = os.path.dirname(__file__)

sys.path.append(BASEDIR)

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings_test'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(sys.argv[1:])
    sys.exit(bool(failures))
