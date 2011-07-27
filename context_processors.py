from django import forms
from django.contrib.auth.models import User
from django.conf import settings

def switch_user(request):
	"""
	Create a form and pass it into the context, for super users.

	This form is a single field, where a super user can change
	to another user to see how the page looks for them.
	"""

	if request.user.is_superuser or request.user.has_perm('Switch User') or \
		(request.session and request.session.has_key('superuser-switch')):

		class SelectUser(forms.Form):
			user = ModelChoiceField(queryset=User.objects.all())

		return {'switch_user_form': SelectUser(prefix="django-switch") }
	return {}
