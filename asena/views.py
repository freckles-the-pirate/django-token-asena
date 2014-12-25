from django.shortcuts import render
from django.conf import settings
from asena.models.token import Token, InvalidTokenException
from asena.models.token import AutorizationException, DisabledTokenException
from django.http import HttpResponseRedirect

def get_setting(setting, alt_value):
    try:
        return settings.setting
    except Exception:
        return alt_value

def token_prompt(request, *args, **kwargs):
    template_needed = get_setting(ASENA_TOKEN_NEEDED_TEMPLATE,            
                                    'token_needed.html')
    template_invalid = get_setting(ASENA_TOKEN_INVALID_TEMPLATE,
                                   'token_invalid.html')
    template_disabled = get_setting(ASENA_TOKEN_INCORRECT_TEMPLATE,
                                     'token_disabled.html')
    context = {}
    e = kwargs['exception']
    if isinstance(e, InvalidTokenException):
        context.update({'token_value' : e.token})
        return render(request, template_invalid, context)
    elif isinstance(e, AutorizationException):
        return render(request, template_needed, context)
    context.update({'token_value' : e.token})
    return render(request, template_disabled, context)

def token_protect(redirect_view=token_prompt):
    """ Only allow the user to access the page if a token is given.
    
    :param redirect: (optional). Redirect the view to ``redirect``. Default
        is asena.views.token_prompt.
    :type redirect: def
    
    :return: A view function; ``decorate.call`` if the token given is valid or 
        ``redirect`` if the token is invalid.
    """
    def wrap(view_func):
        def _wrapped_view_func(request, *args, **kwargs):
            try:
                result = Token.request_is_valid(request)
            except InvalidTokenException as e1:
                kwargs.update({'exception', e1})
                return redirect_view(request, *args, **kwargs)
            except AutorizationException as e2:
                kwargs.update({'exception', e2})
                return redirect_view(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)     
        return _wrapped_view_func
    return wrap