from django.shortcuts import render, redirect
from django.conf import settings
from asena.models.token import Token, TokenException, InvalidTokenException
from asena.models.token import AuthorizationException, DisabledTokenException
from django.http import HttpResponseRedirect

from asena.logger_setup import *
import logging
logger = logging.getLogger('test_logger')
import pprint

def get_setting(setting, alt_value):
    if hasattr(settings, setting):
        return settings.setting
    return alt_value

def token_prompt(request, *args, **kwargs):
    template_needed = get_setting('ASENA_TOKEN_NEEDED_TEMPLATE',
                                    'token_needed.html')
    template_invalid = get_setting('ASENA_TOKEN_INVALID_TEMPLATE',
                                   'token_invalid.html')
    template_disabled = get_setting('ASENA_TOKEN_INCORRECT_TEMPLATE',
                                     'token_disabled.html')
    context = {}
    e = kwargs['exception']
    
    # Get the url to which we want to redirect.
    if request.method == 'POST' and 'next' in request.POST:
        next = request.POST['next']
    elif request.method == 'GET' and 'next' in request.GET:
        next = request.GET['next']
        
    # If we've encountered a "Token exception", use the appropriate template.
    if isinstance(e, InvalidTokenException):
        context.update({'token_value' : e.token})
        return render(request, template_invalid, context)
    elif isinstance(e, AuthorizaonException):
        return render(request, template_needed, context)
    elif isinstance(e, DisabledTokenException):
        context.update({'token_value' : e.token})
        return render(request, template_disabled, context)
    
    # Otherwise, simply return the view.
    return redirect(request.GET['next'])

def token_protect(redirect_view=token_prompt):
    """ Only allow the user to access the page if a token is given.
    
    :param redirect: (optional). Redirect the view to ``redirect``. Default
        is asena.views.token_prompt.
    :type redirect: def
    
    :return: A view function; ``decorate.call`` if the token given is valid or 
        ``redirect`` if the token is invalid.
    """
    logger.debug("token_protect(%s)"%redirect_view)
    def wrap(view_func):
        logger.debug("In wrap(%s)"%type(view_func))
        def _wrapped_view_func(request, *args, **kwargs):
            logger.debug("request type: %s"%type(request))
            logger.debug("args: %s"%pprint.pformat(args))
            logger.debug("kwargs: %s"%pprint.pformat(kwargs))
            # Here we'll check to see if the token is valid. If an exception is
            # thrown, pass it to ``redirect_view``.
            try:
                logger.debug("Testing if request is valid...")
                result = Token.request_is_valid(request)
            except TokenException as e1:
                logger.error("%s"%type(e1))
                kwargs.update({'exception' : e1})
                return redirect_view(request, *args, **kwargs)
            return view_func
        return _wrapped_view_func
    return wrap