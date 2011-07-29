==================
DJANGO SWITCH USER
==================
Simple app that places a small form for super users to select a different user, and 
automatically log in as that user, for testing purposes.

settings.py
-----------
::

	INSTALLED_APPS = (
		...
		'django_switch_user',
	)


Note that the order of middleware is important. 
Take care to place this before any user-dependent middleware.
If you are using Django's CSRF middleware, the SwitchUser
middleware must come AFTER CSRF middleware.::

	MIDDLEWARE_CLASSES = (
		...
                'django.middleware.csrf.CsrfViewMiddleware',
		'django_swtich_user.middleware.SwitchUser',
	)

By default, the auth backends contains only Django's Modelbackend.
Include that one as well when you override the setting.::

	AUTHENTICATION_BACKENDS = (
		'django.contrib.auth.backends.ModelBackend',
		'django_switch_user.backends.SwitchUserBackend',
	)