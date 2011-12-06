from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django import forms
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode, DjangoUnicodeDecodeError

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
			new_username = None
			new_user = None
			
			if 'django-switch-user-go-back' in request.POST:
				new_username = request.session['switch-user-original-user'].username
			elif request.POST['django-switch-user']: 
				# Didn't we already check for this being in request.POST? Yes. But we did not check the boolean value of it.
				new_username = User.objects.get(id=request.POST['django-switch-user']).username

			if new_username:
				new_user = authenticate(original_username=request.user.username, new_username=new_username, auth_session=True)

			if new_user:
				
				"""
				Say you switch from user A to B to ... to Y to Z:
				original_user: This is user A
				previous_user: This is user Y
				new_user:      This is user Z
				"""

				previous_user = request.user

				original_user = previous_user
				if request.session.has_key('switch-user-original-user'):
					original_user = request.session['switch-user-original-user']

				"""
				Perform the switch
				"""

				login(request,new_user)

				request.user = new_user
				request.session['_auth_user_id'] = new_user.id
				request.session['switch-user-original-user'] = original_user

				"""
				Erase the original user flag if you switch back to 
				the original user
				"""

				if request.session.has_key('switch-user-original-user') and request.session['switch-user-original-user'] == new_user:
					del request.session['switch-user-original-user']

				"""
				Here, we flag the session, so that switching to a user
				without permission to switch back, will still allow
				you to switch back.
				"""

				request.session['switch-user-flag'] = True


				return redirect(request.path)

		return

	def is_auth_to_switch(self,request):
		if not hasattr(request,'session'):
			return False

		if request.user.is_superuser or request.user.has_perm('Switch User') or \
				request.session.has_key('switch-user-flag'):
			return True
		return False

	def response_has_content(self,response):
		try:
			response.content
		except TypeError:
			return False
		else:
			return True

	def process_response(self,request,response):

		"""
		Embed the form template into the response content
		"""

		if self.is_auth_to_switch(request) and self.response_has_content(response) and response.content.lower().rfind("</body>") >= 0:

			form = self.get_form()

			context = {
					"switch_user_form": form(prefix=self.get_form_prefix()),
					"switch_user_current_user": self.get_user_label(request.user) }

			if 'csrftoken' in request.COOKIES:
				context['csrf_token'] = request.COOKIES['csrftoken']

			if request.session.has_key('switch-user-original-user'):
				context['switch_user_original_user'] = self.get_user_label(request.session['switch-user-original-user'])

			try:

				response.content = replace_insensitive(
					smart_unicode(response.content),
					u'</body>',
					smart_unicode(render_to_string(self.get_template(),context) + u'</body>')
				)
			except DjangoUnicodeDecodeError:
				"""
				This usually happens when a file is being passed in from the response. This needs to be addressed more specifically...
				"""
				pass

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
		To override the display of users in the form, create a function 
		in your settings.py file called DJANGO_SWITCH_USER_LABEL. It
		must take one argument, which will be the User model. It must
		return a string representation of the user.
		"""
		if hasattr(settings, 'DJANGO_SWITCH_USER_LABEL'):
			return settings.DJANGO_SWITCH_USER_LABEL(user)
		return "%s" % user

	def get_form_prefix(self):
		return "django-switch"

	def get_template(self):
		return "django_switch_user/switch_user_form.html"
