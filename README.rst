==================
DJANGO SWITCH USER
==================
Simple app that places a small form for super users to select a different user, and 
automatically log in as that user, for testing purposes.

INSTALLATION (settings.py)
-------------------------
::

	INSTALLED_APPS = (
		...
		'django_switch_user',
	)


Note that the order of middleware is important. 
Take care to place this before any user-dependent middleware.
If you are using Django's CSRF middleware, the SwitchUser
middleware must come AFTER CSRF middleware. ::

	MIDDLEWARE_CLASSES = (
		...
        'django.middleware.csrf.CsrfViewMiddleware',
        'django_swtich_user.middleware.SwitchUser',
    )

By default, the auth backends contains only Django's Modelbackend.
Include that one as well when you override the setting. ::

	AUTHENTICATION_BACKENDS = (
		'django.contrib.auth.backends.ModelBackend',
		'django_switch_user.backends.SwitchUserBackend',
	)

CUSTOMIZATION (settings.py)
-------------------------

If you would like to customize the queryset of users in the form ::

    def DJANGO_SWITCH_USER_QUERYSET(qs):
        return qs.filter(is_active=True).order_by('last_name')

If you would like to customize the display of users in the form ::

    def DJANGO_SWITCH_USER_LABEL(u):
        return "%s, %s" % (u.last_name, u.first_name)
