import sys; import os

sys.path.insert(0, os.path.abspath('..'))

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

PROJ_ROOT=os.path.abspath(__file__)
os.putenv('PROJ_ROOT', PROJ_ROOT)
