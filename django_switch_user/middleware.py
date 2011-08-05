from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode
from django.views.decorators.csrf import csrf_exempt

def replace_insensitive(string, target, replacement):
	"""
	Similar to string.replace() but is case insensitive
	Taken from Django Debug Toolbar
	"""
	no_case = string.lower()
	index = no_case.rfind(target.lower())
	if index >= 0:
		return string[:index] + replacement + string[index + len(target):]
	else: # no results so return the original string
		return string

class SwitchUser():
	def process_request(self,request):

		"""
		If the switch user form has been submitted, validate that the user
		is either a superuser, or they have the correct session flag
		(which is set below when needed). We use a custom auth backend to
		'validate' the user

		This requires the use of sessions.
		"""

		if request.POST and 'django-switch-user' in request.POST and self.is_auth_to_switch(request):
					
			new_username = User.objects.get(id=request.POST['django-switch-user']).username

			if request.session.has_key('superuser-switch'):
				new_user = authenticate(original_username=request.user.username, new_username=new_username, superuser_session=True)
			else:
				new_user = authenticate(original_username=request.user.username, new_username=new_username)
			
			login(request,new_user)

			request.user = new_user
			request.session['_auth_user_id'] = new_user.id

			"""
			We put a flag variable on the session, so we know this session belongs 
			to a super user. This way, process_response knows to display the form
			to switch users again.
			"""

			request.session['superuser-switch'] = True

			return redirect(request.path)

		return

	def is_auth_to_switch(self,request):
		if isinstance(request, WSGIRequest) or not hasattr(request,'session'):
			return False

		if request.user.is_superuser or request.user.has_perm('Switch User') or \
				request.session.has_key('superuser-switch'):
			return True
		return False

	def process_response(self,request,response):
		"""
		Embed the form template into the response content
		"""
		if self.is_auth_to_switch(request):

			form = self.get_form()

			context = {self.get_context_var_name(): form(prefix=self.get_form_prefix()) }

			if 'csrftoken' in request.COOKIES:
				context['csrf_token'] = request.COOKIES['csrftoken']

			response.content = replace_insensitive(
				smart_unicode(response.content),
				u'</body>',
				smart_unicode(render_to_string(self.get_template(),context) + u'</body>')
			)

			if response.get('Content-Length', None):
				response['Content-Length'] = len(response.content)

		return response

	def get_user_queryset(self):
		"""
		To override the queryset of users in the form, create a function
		in your settings.py file called DJANGO_SWITCH_USER_QUERYSET. It 
		must take one argument, which will be the queryset of all users.
		It must also return a queryset.
		"""

		if hasattr(settings, 'DJANGO_SWITCH_USER_QUERYSET'):
			return settings.DJANGO_SWITCH_USER_QUERYSET(User.objects.all())

		return User.objects.filter(is_active=True).order_by('username')[:100]

	def get_form(self):
		class SelectUser(forms.Form):
			user = forms.ModelChoiceField(queryset=self.get_user_queryset())
			user.label_from_instance = self.get_user_label
		return SelectUser

	def get_user_label(self,user):
		"""
		To override the display of users in the form, create afunction 
		in your settings.py file called DJANGO_SWITCH_USER_LABEL. It
		must take one argument, which will be the User model. It must
		return a string representation of the user.
		"""
		if hasattr(settings, 'DJANGO_SWITCH_USER_LABEL'):
			return settings.DJANGO_SWITCH_USER_LABEL(user)
		return "%s" % user

	def get_context_var_name(self):
		return "switch_user_form"

	def get_form_prefix(self):
		return "django-switch"

	def get_template(self):
		return "django_switch_user/switch_user_form.html"
