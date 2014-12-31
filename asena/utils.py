import random

from asena.logger_setup import *
import logging
logger = logging.getLogger('test_logger')
import pprint

def random_chars(char_set, length):
    """ Choose random characters from a set.
    
    :param char_set: The character set.
    :type char_set: str
    
    :param length: the length of the set.
    :type length: int
    
    :return: A string of random characters chosen from char_set.
    """
    s = ""
    sz = len(char_set)-1
    r = random.SystemRandom()
    for i in range(0, length):
        n = r.randint(0, sz)
        s = s + char_set[n]
    return s

def get_setting(setting, alt_value):
    if hasattr(settings, setting):
        return settings.setting
    return alt_value

def make_url(base, **kwargs):
    sep = '?'
    logger.debug("Making URL with %s and %s"%(base, pprint.pformat(kwargs)))
    for k,v in kwargs.items():
        base = str(base + sep + k + '=' + v)
        if sep == '?':
            sep = '&'
    return base