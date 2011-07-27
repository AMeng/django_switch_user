from django.contrib.auth.models import User

class SwitchUser:
	def process_request(self,request):
		if (request.user.is_superuser or request.session.has_key('superuser-switch')) and \
			request.POST and 'django-switch-user' in request.POST:
				
			"""
			We put a flag variable on the session, so we know this session belongs 
			to a super user. This way, the context processor knows to display the
			form to switch users again.
			"""
			request.session['superuser-switch'] = True

			# Switch the user
			user = User.objects.get(id=request.POST['django-switch-user'])
			request.session['_auth_user_id'] = user.id
			request.user = user

			"""
			Here, we clear out request.POST. We want the regular view to run, but
			not with a (mostly) empty request.POST. This avoids problems where
			the view checks "if request.POST" and then does something special.
			This only happens during the actual user switch process. It does not
			effect POSTing as the new user later on.
			"""

			request.POST._mutable = True
			request.POST.clear()

		return
