from django.shortcuts import render, redirect
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.http import require_POST, require_GET

import string, pprint

from asena.models.token import Token, TokenException, InvalidTokenException
from asena.models.token import AuthorizationException, DisabledTokenException
from asena.forms import TokenWall
from asena.utils import *

from django.conf import settings

logger = logging.getLogger('test_logger')

@require_GET
def token_ajax_generate(request, *args, **kwargs):
    """ Generate token text (not an actual token, though) and return the
    text as an ajax response.
    
    TODO: Make the default length of "10" a setting.
    """
    
    length = int(kwargs.pop('length', 10))
    charset = string.ascii_letters + string.digits
    
    return HttpResponse(random_chars(charset, length))

def token_wall(request, *args, **kwargs):
    context = {}
    
    token_form = TokenWall()
    
    template = get_setting('ASENA_TOKEN_WALL_TEMPLATE', 'token_wall.html')
    
    context.update({'token_wall_form' : token_form})
    
    if request.method == 'GET' and 'token' in request.GET:
        context.update({'token', request.GET['token']})
    elif request.method == 'POST' and 'token' in request.POST:
        context.update({'token', request.GET['token']})
        
    return render(request, template, context)

"""
" Yes, I know I need to use `reverse` to get the URL, but if the asena URLs are 
" included in a project's URLs, Django complains that the URLs are empty 
" because of a circular import. This constant gets around that.
"""
TOKEN_WALL_URL='/token_wall/'

def token_protect(redirect_url=TOKEN_WALL_URL):
    """ Only allow the user to access the page if a token is given.
    
    :param redirect_url: (optional). Redirect the view to ``redirect``. Default
        is '/tokenwall?next=<url>'
    :type redirect: def
    
    :return: A view function; ``decorate.call`` if the token given is valid or 
        ``redirect`` if the token is invalid.
    """
    
    logger.debug("In token_protect('%s')..."%redirect_url)
    
    def wrap(view_func, _redirect_url=redirect_url):
        logger.debug("In wrap(%s)"%view_func)
        def _wrapped_view_func(request, _redirect_url=_redirect_url, *args, 
            **kwargs):
            logger.debug("In _wrapped_view_func()...")
            logger.debug("request type: %s"%type(request))
            logger.debug("args: %s"%pprint.pformat(args))
            logger.debug("kwargs: %s"%pprint.pformat(kwargs))
            
            # Here we'll check to see if the token is valid. If an exception is
            # thrown, return a redirect.
            try:
                logger.debug("Testing if request is valid...")
                result = Token.request_is_valid(request)
            except TokenException as e1:
                logger.error("%s"%type(e1))
                if e1.token:
                    return redirect(make_url(redirect_url,
                                reason=e1.__class__.__name__,
                                token=e1.token.value,
                                next=request.get_full_path()))
                else:
                    return redirect(make_url(redirect_url,
                            reason=e1.__class__.__name__,
                            next=request.get_full_path()))
            
            # If everything checks out, return the view function.
            return view_func(request, *args, **kwargs)
        return _wrapped_view_func
    return wrap