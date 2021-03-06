Django Token Asena
==================

Another Token App?
------------------

Yes, and no. I was looking for an app that would generate a random
string of text for a user, so that a user can view restircted
information on a site without needing a session linked to his username.
What I found on PyPI was good, but not what I needed for a few reasons.

-   The app usually was REST-based, meaning it was more for request
    authentication an not for session authentication.
-   The app relied to heavily on Django's authenticatino system. While
    that potentially could work the problem here is that if you log out
    of the user account, the token session dies with it.

Thus, I have **Django Token Asena**, the app that can provide
session-independent tokens. You can even generate *sets* of tokens. With
each token and with each token set you can set a token expiration and a
token timeout.

Installation
------------

As with most apps, the easiest way is through PIP:

    pip install -U django-token-asena

Add `asena` to your list of `INSTALLED_APPS`:

    INSTALLED_APPS = (
        # ...
        'asena',
        # ...
    )

Contribute
----------

You can contribute to the code at
[Gitorious](https://gitorious.org/django-token-asena). If you have any
questions, please don't hesitate to send me a message!

Other Notes
-----------

### Failed Tests

Some of the unit tests do fail, mainly `test_get_time_remaining`
:   and (consequently) `test_get_session_dict` (both from the
    `asena.tests.test_models.TestToken.` test case). This is because
    there is a clock cycle delay between the expected time and the
    result time, so the values are usually off by a second even if the
    test would normally pass. I'll work on a fix for this in the future.


