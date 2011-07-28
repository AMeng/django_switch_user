from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class SwitchUser():
	def process_request(self,request):

		"""
		If the switch user form has been submitted, validate that the user
		is either a superuser, or they have the correct session flag
		(which is set below when needed). We use a custom auth backend to
		'validate' the user
		"""

		if (request.user.is_superuser or request.session.has_key('superuser-switch')) and \
			request.POST and 'django-switch-user' in request.POST:
			
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
			to a super user. This way, the context processor knows to display the
			form to switch users again.
			"""

			request.session['superuser-switch'] = True

		return

