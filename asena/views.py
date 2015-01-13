from django.shortcuts import render, redirect
from django.conf import settings
from django.core.exceptions import PermissionDenied
#from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST, require_GET

import string, pprint

from asena.models import Token, TokenException, InvalidTokenException
from asena.models import AuthorizationException, DisabledTokenException
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
    
    response = JsonResponse(random_chars(charset, length))
    
    if get_setting('ALLOW_CORS_FOR_TESTING', False):
        response['Access-Control-Allow-Origin' : '*']
    

def token_set_ajax_generate(request, *args, **kwargs):
    
    logger.debug("kwargs: %s"%(pprint.pformat(kwargs)))
    
    count = int(kwargs.pop('count', -1))
    length = int(kwargs.pop('length', -1))
    charset = string.ascii_letters + string.digits
    
    if count < 1:
        count = 1
    if length < 1:
        length = 1
        
    token_set = [random_chars(charset, length) for i in range(0, count)]
    #token_set = [i for i in range(0, count)]
        
    return HttpResponse(','.join(token_set))
    

def token_wall(request, *args, **kwargs):
    context = {}
    
    token_form = TokenWall()
    
    template = get_setting('ASENA_TOKEN_WALL_TEMPLATE', 'token_wall.html')
    
    context.update({'token_wall_form' : token_form})
    
    if request.method == 'GET' and 'token' in request.GET:
        context.update({'token' : request.GET['token']})
    elif request.method == 'POST' and 'token' in request.POST:
        context.update({'token' : request.POST['token']})
        
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
        
        def _wrapped_view_func(request, _redirect_url=_redirect_url, *args, 
            **kwargs):
                
            session_key = get_default_setting('ASENA_SESSION_NAME')
            
            # First check if the user has already entered a token and the token
            # is accepted (hint: check the session). If this is the case, just
            # return the view.
            
            if session_key in request.session:
                if request.session.get_expiry_age() > 0:
                    return view_func(request, *args, **kwargs)
            
            # Here we'll check to see if the token is valid. If an exception is
            # thrown, return a redirect.
            
            logger.debug("Testing if request is valid...")
            if request.method == 'POST':
                token_wall = TokenWall(request.POST)
            elif request.method == 'GET':
                token_wall = TokenWall(request.GET)
            else:
                raise PermissionDenied('Expected either GET or POST.')
            
            token = token_wall.get_token()
                
            if token:
                logger.debug("Token %s checks out!"%token)
                expiry = token.get_session_expiry()
                request.session[session_key] = t
                if expiry:
                    request.session[session_key].set_expiry(expiry)
            
            # If everything checks out, return the view function.
            return view_func(request, *args, **kwargs)
        return _wrapped_view_func
    return wrap