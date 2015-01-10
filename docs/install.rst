===================
Install Token Asena
===================

Initial Install
===============

PIP
---

Probably the easiest and most fun ("fun" meaning "standard"). Type::

    pip install token_asena
    
From Source
------------

If you have the source tarball handy, go into the directory and type::

    make install
    
Configuration
=============

In your django project add the following to installed_apps::

    INSTALLED_APPS = (
        # ...
        'asena',
        # ...
    )
    
Templates
----------

No template is given for the token wall. The expected template is called 
``token_wall.html``. In future versions you'll be able to edit this value in 
the settings.

The form for the token wall will be stored in the variable ``token_form``.

Static Files
------------

``tokenGeneration.js`` is used for the admin form. Run::

    python manage.py collectstatic
    
to collect Token Asena's static files.

Protecting a View
==================

To protect a view, add the ``@token_protect()`` decorator, e.g.

.. code:: python

    from asena.views import token_protect
    
    @token_protect()    # <== Notice the extra parens: ()
    def secret_information(request):
        return render(request, "secret_template.html")
        
The view will be redirected to
'*site_name*/token_wall?reason= *reason*&next= *original URL*'.

To override the URL to which the view is redirected, add the following to 
your site's ``urls.py``:

.. code:: python

    url(r'^some_path/$', asena.views.token_wall, name="token_wall"),
    
Where ``some_path`` is the name of the URL.