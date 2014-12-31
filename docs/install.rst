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
    
You'll need to add a custom URL, too. Open your ``urls.py`` file and add::

    url(r'^/tokenwall/$', """ Add your own view here! """),
    
